var cannlytics=function(e){var t={};function n(r){if(t[r])return t[r].exports;var o=t[r]={i:r,l:!1,exports:{}};return e[r].call(o.exports,o,o.exports,n),o.l=!0,o.exports}return n.m=e,n.c=t,n.d=function(e,t,r){n.o(e,t)||Object.defineProperty(e,t,{enumerable:!0,get:r})},n.r=function(e){"undefined"!=typeof Symbol&&Symbol.toStringTag&&Object.defineProperty(e,Symbol.toStringTag,{value:"Module"}),Object.defineProperty(e,"__esModule",{value:!0})},n.t=function(e,t){if(1&t&&(e=n(e)),8&t)return e;if(4&t&&"object"==typeof e&&e&&e.__esModule)return e;var r=Object.create(null);if(n.r(r),Object.defineProperty(r,"default",{enumerable:!0,value:e}),2&t&&"string"!=typeof e)for(var o in e)n.d(r,o,function(t){return e[t]}.bind(null,o));return r},n.n=function(e){var t=e&&e.__esModule?function(){return e.default}:function(){return e};return n.d(t,"a",t),t},n.o=function(e,t){return Object.prototype.hasOwnProperty.call(e,t)},n.p="",n(n.s=0)}([function(e,t,n){n(1),e.exports=n(2)},function(e,t,n){"use strict";n.r(t),t.default=n.p+"./css/bundle.css"},function(e,t,n){"use strict";function r(e,t){var n=Object.keys(e);if(Object.getOwnPropertySymbols){var r=Object.getOwnPropertySymbols(e);t&&(r=r.filter((function(t){return Object.getOwnPropertyDescriptor(e,t).enumerable}))),n.push.apply(n,r)}return n}function o(e){for(var t=1;t<arguments.length;t++){var n=null!=arguments[t]?arguments[t]:{};t%2?r(Object(n),!0).forEach((function(t){a(e,t,n[t])})):Object.getOwnPropertyDescriptors?Object.defineProperties(e,Object.getOwnPropertyDescriptors(n)):r(Object(n)).forEach((function(t){Object.defineProperty(e,t,Object.getOwnPropertyDescriptor(n,t))}))}return e}function a(e,t,n){return t in e?Object.defineProperty(e,t,{value:n,enumerable:!0,configurable:!0,writable:!0}):e[t]=n,e}n.r(t),n.d(t,"payments",(function(){return s})),n.d(t,"website",(function(){return c}));var s={subscribe(e){var t,n=document.getElementById("account-information");n?t=o(o({},t=Object.fromEntries(new FormData(n).entries())),e):t={email:document.getElementById("email-input").value};fetch("/subscribe/",{method:"POST",body:JSON.stringify(t)}),window.location.href="/subscriptions/subscribed/"}},c={initialize(){feather.replace(),this.acceptCookiesCheck(),this.setInitialTheme(),this.scrollToHash()},initializeToasts(){var e=document.getElementById("cookie-toast");new bootstrap.Toast(e,{autohide:!1})},acceptCookies(){localStorage.setItem("acceptCookies",!0);var e=document.getElementById("accept-cookies");e.style.display="none",e.style.opacity=0},acceptCookiesCheck(){if(!localStorage.getItem("acceptCookies")){var e=document.getElementById("accept-cookies");e.style.display="block",e.style.opacity=1}},changeTheme(){var e=localStorage.getItem("theme");if(!e){var t=(new Date).getHours();e=t>6&&t<20?"light":"dark"}var n="light"===e?"dark":"light";this.setTheme(n),localStorage.setItem("theme",n)},setInitialTheme(){if("undefined"!=typeof Storage){var e=localStorage.getItem("theme");if(!e){var t=(new Date).getHours();return void(t>6&&t<20||this.setTheme("dark"))}this.setTheme(e),localStorage.setItem("theme",e)}else document.getElementById("theme-toggle").style.display="none"},setTheme(e){"light"===e?document.body.className="base":this.hasClass(document.body,"dark")||(document.body.className+=" dark")},hasClass:(e,t)=>(" "+e.className+" ").indexOf(" "+t+" ")>-1,scrollToHash(){var e=window.location.hash.substring(1),t=document.getElementById(e);t&&t.scrollIntoView()},copyToClipboard(e){[/<span class="p">/g,/<\/span>/g,/<span class="nx">/g,/<span class="o">/g,/<span class="s2">/g,/<span class="kn">/g,/<span class="n">/g,/<span class="nn">/g].forEach(t=>{e=e.replace(t,"")}),window.prompt("Copy to clipboard: Press Ctrl+C, then Enter",e)},subscribe(){var e=document.getElementById("email-input"),t=document.getElementById("subscribe-button"),n=e.value;if(n){t.disabled=!0;var r=new XMLHttpRequest;r.addEventListener("readystatechange",(function(){4===this.readyState&&(JSON.parse(this.responseText).message.success?(e.value="",document.location.href="/subscribed"):alert("Error subscribing. Please check that your email is valid and that you have a healthy internet connection."),t.disabled=!1)})),r.open("POST","/subscribe"),r.setRequestHeader("Content-Type","application/x-www-form-urlencoded"),r.send("email=".concat(n))}}}}]);
//# sourceMappingURL=bundle.js.map