/**
 * Data JavaScript | Cannlytics Website
 * Copyright (c) 2021-2022 Cannlytics
 * 
 * Authors: Keegan Skeate <contact@cannlytics.com>
 * Created: 8/21/2021
 * Updated: 1/24/2022
 * License: MIT License <https://github.com/cannlytics/cannlytics-website/blob/main/LICENSE>
 */
import { reportError } from '../payments/payments.js';
import { authRequest } from '../utils.js';

export const data = {

  /**
   * Payment
   */

  initializePayPalPayment() {
    /**
     * Initialize PayPal payment option.
     */

    // TODO: Make description dynamic.
    const orderDescription = 'Washington State lab results combined with licensee, inventory, and strain data.';

    paypal.Buttons({
      style: {
        shape: 'pill',
        color: 'gold',
        layout: 'vertical',
        label: 'buynow',
        
      },
      createOrder: function(data, actions) {

        // TODO: Allow user to choose business or student price.
        const priceTotal = 499;

        return actions.order.create({
          purchase_units: [{
            description: orderDescription,
            amount: {
              currency_code: 'USD',
              value: priceTotal,
              breakdown: {
                item_total: {
                  currency_code: 'USD',
                  value: itemTotalValue,
                },
                shipping: {
                  currency_code: 'USD',
                  value: 0,
                },
                tax_total: {
                  currency_code: 'USD',
                  value: 0,
                }
              }
            },
            items: [{
              name: orderDescription,
              unit_amount: {
                currency_code: 'USD',
                value: priceTotal,
              },
              quantity: 1
            }]
          }]
        });
      },
      onApprove: function(data, actions) {
        return actions.order.capture().then(async function(details) {
          
          // Capture payment details.
          const name = details.payer.name.given_name;
          const email = details.payer.email_address;
          const paymentId = details.id;
          const postData = {
            name,
            email,
            payer_id: details.payer.payer_id,
            payment_id: paymentId,
            payment_link: details.links[0].href,
            order_json: JSON.stringify(details),
          };

          // Trigger download, double-checking the payment in the API.
          const response = await authRequest('/src/payments/buy-data', postData);
          if (response.success) {

            // Report payment.
            await reportSubscription(email, name, paymentId);

            // Show a success / thank you message.
            const element = document.getElementById('paypal-button-container');
            element.innerHTML = '';
            document.getElementById('thank-you-message').classList.remove('d-none');

          } else {
            const message = 'An error occurred when buying data. Please try again later or email support.';
            showNotification('Error Subscribing', message, /* type = */ 'error');
          }

        });
      },
      onError: function(error) {
        const message = 'A payment error occurred. Please try again later or email support.';
        showNotification('Payment Error', message, /* type = */ 'error');
        reportError();
      },
    }).render('#paypal-button-container');
  },

  /**
   * Market
   */

  async getDataset(id) {
    /**
     * Get metadata about a given dataset.
     * @param {String} id A dataset ID.
     */
    return await authRequest(`/api/datasets/${id}`);
  },

  async getDataMarketStats() {
    /**
     * Get metadata about the data market.
     */
    return await authRequest('/api/market');
  },

  async getStateData(id) {
    /**
     * Get metadata about a given state's data.
     * @param {String} id A state ID. Typically the lowercase state abbreviation.
     *    e.g. `nc` for North Carolina.
     */
    if (id) return await authRequest(`/api/data/state/${id}`);
    return await authRequest('/api/data/state');
  },

  downloadDataset() {
    /**
     * Download a given dataset.
     */
    authRequest('/api/market/download-lab-data');
  },

  async publishDataset() {
    /**
     * Publish a given dataset on the data market.
     */
    const response = authRequest('/api/market/download-lab-data');
    if (response.success) {
      const message = 'Your dataset has been published.';
      showNotification('Data Published', message, /* type = */ 'success');
    } else {
      const message = 'An error occurred when saving your account.';
      showNotification('Error Publishing Data', message, /* type = */ 'error');
    }
  },

  sellDataset() {
    /**
     * Sell a given dataset on the data market.
     */
    // TODO: Get dataset details from the UI.
    const dataset = {};
    const response = authRequest('/api/market/sell', dataset);
    if (response.success) {
      const message = 'Your dataset is now for sale.';
      showNotification('Data Listed for Sale', message, /* type = */ 'success');
    } else {
      const message = 'An error occurred when listing your data for sale.';
      showNotification('Error Listing Data for Sale', message, /* type = */ 'error');
    }
  },

  buyDataset() {
    /**
     * Buy a given dataset on the data market.
     */
    // TODO: Get dataset details from the UI.
    const dataset = {};
    const response = authRequest('/api/market/buy', dataset);
    if (response.success) {
      const message = 'Your have successfully bought a dataset.';
      showNotification('Data Purchased', message, /* type = */ 'success');
    } else {
      const message = 'An error occurred when purchasing this dataset.';
      showNotification('Error Purchasing Data', message, /* type = */ 'error');
    }
  },

};
