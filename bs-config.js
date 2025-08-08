/**
 * BrowserSync Configuration
 *
 * For more options, see: http://www.browsersync.io/docs/options/
 */
module.exports = {
   // Your local development URL for the WordPress site
   proxy: "127.0.0.1:8000",

   // The files to watch for changes
   files: [
      'static/css/*.css', 'static/js/*.js', 'core/templates/**/*.html'
   ],

   // Inject CSS changes without reloading the page
   injectChanges: true,

   // Don't show the "Connected to BrowserSync" notification
   notify: false,

   // Disable ghost mode (prevents mirroring of clicks, scrolls, etc.)
   ghostMode: false,

   // Open the site in the browser automatically
   open: false,

   // Change the port from the default 3000 to 3001 to avoid potential conflicts
   port: 3000
};