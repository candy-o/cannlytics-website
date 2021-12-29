/**
 * Account JavaScript | Cannlytics Website
 * Copyright (c) 2021 Cannlytics
 * 
 * Authors: Keegan Skeate <contact@cannlytics.com>
 * Created: 11/28/2021
 * Updated: 12/27/2021
 * License: MIT License <https://github.com/cannlytics/cannlytics-website/blob/main/LICENSE>
 */
import {
  changeEmail,
  getCurrentUser,
  onAuthChange,
  updateUserPhoto,
  updateUserDisplayName,
} from '../firebase.js';
import {
  authRequest,
  deserializeForm,
  serializeForm,
  showNotification,
} from '../utils.js';

export const accountSettings = {

  chooseUserPhoto() {
    /**
     * Choose a file to upload.
     */
    document.getElementById('user-photo-url').click();
  },

  initializeAccountForm() {
    /**
     * Initialize the user account form.
     */
     onAuthChange(user => {
      if (user) {
        const fileElem = document.getElementById('user-photo-url');
        fileElem.addEventListener('change', this.uploadUserPhoto, false);
        document.getElementById('account-photo').src = user.photoURL;
        const userData = {
          name: user.displayName,
          email: user.email,
          phone_number: user.phoneNumber || '',
        };
        const userForm = document.forms['user-form'];
        userForm.reset();
        deserializeForm(userForm, userData);
      } else {
        window.location.href = `${window.location.origin}/account/sign-up`;
      }
    });
  },

  async saveAccount() {
    /**
    * Saves a user's account fields.
    */
    // FIXME: API returns 500 error.
    const user = getCurrentUser();
    const data = serializeForm('user-form');
    if (data.email !== user.email) {
      await changeEmail(data.email);
    }
    if (data.name !== user.displayName) {
      await updateUserDisplayName(data.name);
    }
    const response = await authRequest('/api/users', data);
    if (response.success) {
      const message = 'Your account data has been successfully saved.'
      showNotification('Account saved', message, /* type = */ 'success');
    } else {
      const message = 'An error occurred when saving your account.'
      showNotification('Error saving your account', message, /* type = */ 'error');
    }
  },

  async uploadUserPhoto() {
    /**
     * Upload a user's photo through the API.
     */
    // FIXME: API error.
    if (this.files.length) {
      showNotification('Uploading photo', 'Uploading your profile picture...', /* type = */ 'wait');
      const downloadURL = await updateUserPhoto(this.files[0]);
      const response = await authRequest('/api/users', { photo_url: downloadURL });
      if (response.success) {
        document.getElementById('user-photo-url').src = downloadURL;
        document.getElementById('user-photo').src = downloadURL;
        const message = 'Successfully uploaded your profile picture.';
        showNotification('Uploading photo complete', message, /* type = */ 'success');
      } else {
        showNotification('Photo Change Error', response.message, /* type = */ 'error');
      };
    }
  },

};
