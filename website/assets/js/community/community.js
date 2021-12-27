/**
 * Community Page JavaScript | Cannlytics Website
 * Copyright (c) 2021 Cannlytics
 * 
 * Authors: Keegan Skeate <keegan@cannlytics.com>
 * Created: 1/17/2021
 * Updated: 11/23/2021
 * License: MIT License <https://github.com/cannlytics/cannlytics-website/blob/main/LICENSE>
 */
import { authRequest, showNotification } from '../utils.js';

export const community = {

  // State

  map: null,
  points: {},
  markerOrange: 'https://firebasestorage.googleapis.com/v0/b/cannlytics.appspot.com/o/public%2Fimages%2Fmaps%2Fmarkers%2Fmarker-orange.png?alt=media&token=264e0fe3-30db-4dd2-be61-8d6e46e5dcea',
  markerGreen: 'https://firebasestorage.googleapis.com/v0/b/cannlytics.appspot.com/o/public%2Fimages%2Fmaps%2Fmarkers%2Fmarker-green.png?alt=media&token=0d4813e6-c9c9-4b21-9b4f-b9879750438a',

  // Functions

  async initialize() {
    /**
     * Initialize the community page.
     */
    
    // Draw the map.
    this.map = this.createMap();

    // Create marker spiderfier for overlapping markers.
    const oms = new OverlappingMarkerSpiderfier(this.map, {
      markersWontMove: true,
      markersWontHide: true,
      basicFormatEvents: true,
      ignoreMapClick: true,
    });

    // Get all of the labs.
    const data = await this.getLabs();

    // Create info windows for each lab.
    const markers = this.createInfoWindows(this.map, oms, data);

    // Cluster dense markers.
    this.createMarkerClusterer(this.map, markers);

    // Wire up search.
    this.setupSearch(this.map);

  },

  createMap() {
    /**
     * Render a Google map.
     * @returns {Map}
     */
    return new google.maps.Map(document.getElementById('map'), {
      zoom: 4,
      center: new google.maps.LatLng(39.8283, -98.5795),
      gestureHandling: 'greedy',
      mapTypeId: google.maps.MapTypeId.ROADMAP,
    });
  },

  createInfoWindows(map, oms, data) {
    /**
     * Create markers with info windows.
     * @param {Map} map The Google map.
     * @param {OverlappingMarkerSpiderfier} oms Overlapping marker spiderfier.
     * @param {Array} data A list of data used in creating info-windows.
     * @returns {Array}
     */
    // var logSearch = this.logSearch;
    var createWindow = this.createMarkerInfoWindow;
    var infowindow = new google.maps.InfoWindow();
    var markers = [];
    var searchOptions = '';
    data.forEach((item, index) => {

      // Alternate marker colors.
      // TODO: Use green for DEA registered hemp testing laboratories.
      // https://www.ams.usda.gov/rules-regulations/hemp/dea-laboratories
      var icon;
      if (index % 2) icon = this.markerOrange;
      else icon = this.markerOrange;     

      // Create marker.
      var marker = new google.maps.Marker({
        icon: icon,
        position: new google.maps.LatLng(item.latitude, item.longitude),
        map: map,
        title: item.name,
      });

      // Open infowindow on click.
      google.maps.event.addListener(marker, 'spider_click', ((marker) => {
        return function() {

          // Ensure that the website is valid.
          var url = item.website;
          if (url) {
            if (!url.startsWith('http')) {
              url = `http://${url}`;
            }
          }
          
          // Ensure that the image URL is valid.
          if (item.image_url) {
            if (!item.image_url.startsWith('http') && url) {
              item.image_url = `${url}${item.image_url}`;
            }
          }
          
          // Format the content.
          var content = createWindow(item);

          // Attach the content to the infowindow.
          infowindow.setContent(content);
          infowindow.open(map, marker);

          // Log which labs are viewed.
          // logSearch(item.id, 'window_views');
        }
      })(marker));

      // Add marker to list of markers.
      markers.push(marker);
      oms.addMarker(marker);
      var name = item.trade_name ?? item.name;
      this.points[name] = { latitude: item.latitude, longitude: item.longitude };
      searchOptions += `<option value="${name}"/>`;
    });

    // Close infowindow on map click.
    google.maps.event.addListener(map, 'click', function() {
      infowindow.close();
    });

    // Add lab names to search options.
    document.getElementById('searchOptions').innerHTML = searchOptions;

    // Return the list of markers.
    return markers;

  },

  createMarkerClusterer(map, markers) {
    /**
     * Create a clusterer for markers on the map.
     * @param {Map} map The Google map.
     * @param {Array} markers A list of markers to render.
     * @returns {MarkerClusterer}
     */
    // TODO: replace imagePath with local path.
    return new MarkerClusterer(map, markers, {
      gridSize: 50,
      maxZoom: 10,
      minimumClusterSize: 4,
      imagePath: 'https://developers.google.com/maps/documentation/javascript/examples/markerclusterer/m',
    });
  },

  createMarkerInfoWindow(item) {
    /**
     * Creates a marker info window.
     * @param {Object} item Information to render in the info-window.\
     * @returns {String}
     */
    var name = item.trade_name ?? item.name;
    var content = `<div class="text-dark p-3">`;
    content += `
      <a href="/labs/${item.slug}/" target="_blank">
        <img src="${item.image_url}" class="float-start me-3 mb-3" style="max-width:150px;max-height:75px;">
      </a>
      <h5 class="fs-4 mb-0">
        <a class="text-dark serif open-in-new" href="/labs/${item.slug}/">${name}</a>
      </h5>
      <p class="fs-6 mb-3">
        <small class="text-secondary">${item.formatted_address.replace(', USA', '')}</small>
      </p>
      <div class="d-flex w-100"><p class="fs-6">`;
    if (item.phone) {
      content += `Phone: <a href="tel:${item.phone_number}">${item.phone}</a><br>`;
    } else {
      content += `Phone: <a class="btn btn-sm btn-light" href="/labs/${item.slug}/?edit=true">Recommend a phone number</a><br>`;
    }
    if (item.email) {
      content += `Email: <a href="mailto:${item.email}">${item.email}</a><br>`;
    } else {
      content += `Email: <a class="btn btn-sm btn-light" href="/labs/${item.slug}/?edit=true">Recommend an email</a><br>`;
    }
    if (item.website) {
      var url = item.website;
      if (!url.startsWith('https')) url = `https://${url}`;
      content += `Website: <a href="${url}" target="_blank">${item.website}</a>`;
    } else {
      content += `Website: <a class="btn btn-sm btn-light" href="/labs/${item.slug}/?edit=true">Recommend a website</a><br>`;
    }
    content += `</p></div>`;
    if (item.description) content += `<p class="fs-6 mt-3"><small class="serif">${item.description}</small></p>`
    content += `</div>`;
    // TODO: Add analyses with prices
    return content;
  },

  // Optional: Log which labs people search for.
  // logSearch(id, field) {
  //   /**
  //    * Record when people search or view for a lab.
  //    * @param {String} id The ID for the log.
  //    * @param {String} field The page viewed.
  //    */
  //   const timestamp = new Date().toISOString();
  //   const update = { updated_at: timestamp };
  //   throw new NotImplementedException();
  //   // update[field] = firestore.FieldValue.increment(1);
  //   // updateDocument(`labs/${id}`, update);
  //   // updateDocument(`public/logs/website_logs/${timestamp}`, {
  //   //   action: `Incremented ${field} for ${id}.`,
  //   //   updated_at: timestamp,
  //   // });
  // },

  onInput() {
    /**
     * Pan to a marker on selection.
     */
    var val = document.getElementById('searchInput').value;
    var opts = document.getElementById('searchOptions').childNodes;
    for (var i = 0; i < opts.length; i++) {
      if (opts[i].value === val) {
        this.panToMarker(this.map, opts[i].value)
        break;
      }
    }
  },

  panToMarker(map, value) {
    /**
     * Pan to a point on the map.
     * @param {Map} map The Google map.
     * @param {String} value A value to search for on the map.
     */
    const point = this.points[value];
    map.panTo(new google.maps.LatLng(point.latitude, point.longitude));
    map.setZoom(15);
    // this.logSearch(item.id, 'searches');
  },

  setupSearch(map) {
    /**
     * Setup search for the map.
     * @param {Map} map The Google map.
     */
    var searchButton = document.getElementById('searchButton');
    var searchInput = document.getElementById('searchInput');
    searchButton.addEventListener('click', () => {
      this.panToMarker(map, searchInput.value)
    });
    searchInput.addEventListener('keydown', (event) => {
      if (event.key === 'Enter') {
        this.panToMarker(map, searchInput.value)
      }
    });
  },

  async getLabs() {
    /**
     * Get labs with API.
     * @returns {list}
     */
    return await authRequest('/api/labs');
  },

  showPromo() {
    /**
     * Show the promo code field.
     */
    const promoButton = document.getElementById('promo-button');
    const promoInputGroup = document.getElementById('promo-input-group');
    promoButton.style.display = 'none';
    if (promoInputGroup.classList.contains('visually-hidden')) {
      promoInputGroup.classList.remove('visually-hidden');
    }
  },

  async downloadLabs() {
    /**
     * Download either free or premium data sets.
     */

    // Get any promo code.
    const promoCode = document.getElementById('promo-input').value;

    // Download data.
    const url = `${window.location.origin}/api/labs/download`;
    const time = new Date().toISOString().slice(0, 19).replace(/T|:/g, '-');
    const filename = `labs-${time}.csv`;
    try {
      const res = await fetch(url, {
        method: 'GET',
        headers: {
          Authorization: `Bearer ${promoCode}`
        }
      });
      const blob = await res.blob();
      const newBlob = new Blob([blob]);
      const blobUrl = window.URL.createObjectURL(newBlob);
      const link = document.createElement('a');
      link.href = blobUrl;
      link.setAttribute('download', filename);
      document.body.appendChild(link);
      link.click();
      link.parentNode.removeChild(link);
      window.URL.revokeObjectURL(blob);
    } catch(error) {
      showNotification('Download error', error, /* type = */ 'error' );
    }

    // Hide dialog.
    const downloadDialog = document.getElementById('downloadDialog');
    const modal = bootstrap.Modal.getInstance(downloadDialog);
    modal.hide();

  },

};
