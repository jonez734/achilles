$(document).ready(function() {
    function validateSectionName(name) {
        return name && /^[a-zA-Z0-9_-]+$/.test(name);
    }

    function showError($body, msg) {
        $body.html('<div class="error">' + msg + '</div>').slideDown();
    }

    function loadSectionBody($section) {
        var $body = $section.find('.body');
        var $h1 = $section.find('.header h1');
        var sectionName = $section.data('name');

        return $.ajax({
            url: '/achilles/section.php',
            type: 'GET',
            data: { name: sectionName },
            success: function(data) {
                var $html = $('<div>').html(data);

                var newTitle = $html.find('.header h1, .header h2').text();
                if (newTitle && newTitle.trim()) {
                    $h1.text(newTitle.trim());
                }

                var newBodyContent = $html.find('.body').html();

                if (newBodyContent) {
                    $body.html(newBodyContent);
                } else {
                    $body.html(data);
                }
            },
            error: function() {
                $body.html('<div class="error">Error loading section. Please try again.</div>');
            }
        });
    }

    // Open a section: load body if needed, rotate arrow, slide down.
    // Idempotent: if body already loaded, just slides down. If already visible, no-op.
    function openSection($section) {
        var $arrow = $section.find('.header .arrow');
        var $body = $section.find('.body');
        var sectionName = $section.data('name');

        if (!validateSectionName(sectionName)) {
            showError($body, 'Invalid section.');
            return $.Deferred().reject().promise();
        }

        var applyOpen = function() {
            $arrow.addClass('open');
            if ($body.is(':hidden')) {
                $body.slideDown();
            }
        };

        if ($.trim($body.html()) === '') {
            return loadSectionBody($section).then(applyOpen);
        }
        applyOpen();
        return $.Deferred().resolve().promise();
    }

    // Close a section: rotate arrow off, slide up.
    function closeSection($section) {
        var $arrow = $section.find('.header .arrow');
        var $body = $section.find('.body');
        $arrow.removeClass('open');
        if ($body.is(':visible')) {
            $body.slideUp();
        }
    }

    // Header / arrow click: toggle.
    $('.section .header h1, .section .header .arrow').on('click', function() {
        var $section = $(this).closest('.section');
        var $arrow = $section.find('.header .arrow');
        var sectionName = $section.data('name');

        if (!validateSectionName(sectionName)) {
            showError($section.find('.body'), 'Invalid section.');
            return;
        }

        if ($arrow.hasClass('open')) {
            closeSection($section);
        } else {
            openSection($section);
        }
    });

    // On-load: open sections marked data-open="1" by the server.
    $('.section').each(function() {
        var $section = $(this);
        if ($section.data('open') === 1 || $section.data('open') === '1') {
            openSection($section);
        }
    });

    // Expand-all: open every section so the page can be printed.
    $('[data-expand-all]').on('click', function() {
        var $btn = $(this);
        $btn.prop('disabled', true);
        var $sections = $('.section');
        var jobs = $sections.map(function() {
            return openSection($(this));
        }).get();
        $.when.apply($, jobs).always(function() {
            $btn.prop('disabled', false);
        });
    });
});
