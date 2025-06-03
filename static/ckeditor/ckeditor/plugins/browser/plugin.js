/**
 * Browser Plugin
 *
 * @author Ayhan Akilli
 */
'use strict';

/**
 * Browser
 */
(function (CKEDITOR) {
    /**
     * Plugin
     */
    CKEDITOR.plugins.add('browser', {requires: 'api'});

    /**
     * Initializes all browser buttons on dialog definition
     *
     * A browser button is a button element with a `browser` property that is a callback function and a `browserUrl`
     * property with the URL to the browser page that will be opened in a new window. The `browser` callback function is
     * later executed when this browser window sends a message.
     */
    CKEDITOR.on('dialogDefinition', function (ev) {
        if (!!ev.editor.plugins.browser) {
            CKEDITOR.api.dialog(ev.data.definition, function (item) {
                if (item.type === 'button' && typeof item.browser === 'function' && typeof item.browserUrl === 'string' && !!item.browserUrl) {
                    item.hidden = false;
                    item.onClick = function (ev) {
                        CKEDITOR.api.browser(item.browserUrl, function (data) {
                            ev.sender.browser.call(ev.sender, data);
                        });
                    };
                }
            });
        }
    });
})(CKEDITOR);
