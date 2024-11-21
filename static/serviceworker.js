var staticCacheName = "django-pwa-v" + new Date().getTime();
var filesToCache = [
    // Must Have
    '/offline/',
    '/manifest.json',

    // Images
    '/static/landing_assets/img/auth-offline.gif',
    '/static/landing_assets/img/server.gif',
    '/static/landing_assets/img/logo.png',
    '/static/landing_assets/img/logo-sm.png',
    '/static/pwa_assets/icons/manifest-icon-512.png',
    '/static/pwa_assets/icons/manifest-icon-192.png',
    'static/assets/images/cover-pattern.png',
    '/static/assets/images/error.svg',
    '/static/landing_assets/img/favicon.png',

    // CDN
    'https://fonts.googleapis.com/css?family=Nunito:200,200i,300,300i,400,400i,600,600i,700,700i,800,800i,900,900i',
    'https://cdn.lordicon.com/gsqxdxog.json',
    'https://fonts.gstatic.com/s/poppins/v20/pxiByp8kv8JHgFVrLCz7Z1xlFd2JQEk.woff2',

    // JSON
    '/static/assets/json/country-list.json',

    // CSS
    '/static/assets/js/layout.js',
    '/static/assets/css/bootstrap.min.css',
    '/static/assets/css/icons.min.css',
    '/static/assets/css/app.min.css',
    '/static/assets/css/custom.min.css',
    '/static/assets/libs/multi.js/multi.min.css',
    '/static/admin_assets/fonts/fontawesome5-overrides.min.css',
    '/static/assets/libs/filepond-plugin-image-preview/filepond-plugin-image-preview.min.css',


    // JS
    '/static/assets/libs/bootstrap/js/bootstrap.bundle.min.js',
    '/static/assets/libs/simplebar/simplebar.min.js',
    '/static/assets/libs/node-waves/waves.min.js',
    '/static/assets/libs/feather-icons/feather.min.js',
    '/static/assets/js/pages/plugins/lord-icon-2.1.0.js',
    '/static/assets/js/plugins.js',
    '/static/assets/libs/quill/quill.min.js',
    '/static/assets/libs/sweetalert2/sweetalert2.min.js',
    '/static/assets/libs/%40ckeditor/ckeditor5-build-classic/build/ckeditor.js',
    '/static/assets/libs/nouislider/nouislider.min.js',
    '/static/assets/libs/flatpickr/flatpickr.min.js',
    '/static/assets/libs/%40simonwep/pickr/pickr.min.js',
    '/static/assets/libs/filepond-plugin-image-exif-orientation/filepond-plugin-image-exif-orientation.min.js',
    '/static/assets/libs/wnumb/wNumb.min.js',
    '/static/assets/js/pages/range-sliders.init.js',
    '/static/assets/js/app.js',
    '/static/assets/libs/choices.js/public/assets/scripts/choices.min.js',
    '/static/assets/libs/particles.js/particles.js',
    '/static/assets/js/pages/particles.app.js',


    // WOFF
    '/static/assets/fonts/hkgrotesk-regular.woff',

    // PWA ICON
    '/static/pwa_assets/icons/apple-icon-180.png',
    '/static/pwa_assets/icons/apple-splash-640-1136.jpg',
    '/static/pwa_assets/icons/apple-splash-750-1334.jpg',
    '/static/pwa_assets/icons/apple-splash-1242-2208.jpg',
    '/static/pwa_assets/icons/apple-splash-1125-2436.jpg',
    '/static/pwa_assets/icons/apple-splash-828-1792.jpg',
    '/static/pwa_assets/icons/apple-splash-1242-2688.jpg',
    '/static/pwa_assets/icons/apple-splash-1536-2048.jpg',
    '/static/pwa_assets/icons/apple-splash-1668-2224.jpg',
    '/static/pwa_assets/icons/apple-splash-1668-2388.jpg',
    '/static/pwa_assets/icons/apple-splash-2048-2732.jpg' 
];

// Cache on install
self.addEventListener("install", event => {
    this.skipWaiting();
    event.waitUntil(
        caches.open(staticCacheName)
            .then(cache => {
                return cache.addAll(filesToCache);
            })
            .catch(error => {
                console.error('Caching failed:', error);
            })
    )
});

// Clear cache on activate
self.addEventListener('activate', event => {
    event.waitUntil(
        caches.keys().then(cacheNames => {
            return Promise.all(
                cacheNames
                    .filter(cacheName => (cacheName.startsWith("django-pwa-")))
                    .filter(cacheName => (cacheName !== staticCacheName))
                    .map(cacheName => caches.delete(cacheName))
            );
        })
    );
});

// Serve from Cache
self.addEventListener("fetch", event => {
    event.respondWith(
        caches.match(event.request)
            .then(response => {
                return response || fetch(event.request)
                    .catch(() => {
                        console.log("Offline is found, returning offline page")
                        // If the fetch fails, return the offline page
                        return caches.match('/offline/');
                    });
            })
    )
});

// Register event listener for the 'push' event.
self.addEventListener('push', function (event) {
    const eventInfo = event.data.text();
    const data = JSON.parse(eventInfo);
    const head = data.head || 'New Notification 🕺🕺';
    const body = data.body || 'This is default content. Your notification didn\'t have one 🙄🙄';

    event.waitUntil(
        self.registration.showNotification(head, {
            body: body,
            icon: self.registration.scope + 'static/logo.png'
        })
    );
});