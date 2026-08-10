from playwright.sync_api import sync_playwright


def generate_dashboard_pdf(url, output_path):

    with sync_playwright() as p:

        browser = p.chromium.launch(
            headless=True
        )

        page = browser.new_page(
            viewport={
                "width": 1400,
                "height": 2000
            },
            device_scale_factor=1
        )

        # ============================================================
        # LOAD DASHBOARD
        # ============================================================

        page.goto(
            url,
            wait_until="networkidle"
        )

        # ============================================================
        # USE SCREEN MEDIA
        # ============================================================
        # page.pdf() normally uses print media.
        # Force screen styling so dashboard sections are not hidden
        # or changed by print-specific CSS.

        page.emulate_media(
            media="screen"
        )

        # ============================================================
        # WAIT FOR DASHBOARD CONTENT
        # ============================================================

        page.wait_for_timeout(3000)

        # Wait until the main dashboard is available
        page.wait_for_selector(
            ".dashboard-header",
            timeout=10000
        )

        # ============================================================
        # WAIT FOR CHARTS
        # ============================================================

        page.wait_for_timeout(2000)

        # ============================================================
        # FORCE FULL DOCUMENT HEIGHT
        # ============================================================
        # Prevent dashboard containers/body from clipping content
        # when generating the PDF.

        page.add_style_tag(
            content="""

            html,
            body {

                height: auto !important;

                min-height: 100% !important;

                overflow: visible !important;

            }

            body {

                overflow-y: visible !important;

            }

            .container {

                height: auto !important;

                max-height: none !important;

                overflow: visible !important;

            }

            .dashboard-section {

                height: auto !important;

                max-height: none !important;

                overflow: visible !important;

            }

            .individual-results,
            .improvement-panel,
            .summary-panel,
            .unified-panel {

                height: auto !important;

                max-height: none !important;

                overflow: visible !important;

            }

            .table-wrapper {

                overflow: visible !important;

            }

            """

        )

        # ============================================================
        # WAIT FOR FONT LOADING
        # ============================================================

        page.evaluate(
            """
            async () => {
                if (document.fonts) {
                    await document.fonts.ready;
                }
            }
            """
        )

        # ============================================================
        # FORCE CHARTS TO FINISH RENDERING
        # ============================================================

        page.evaluate(
            """
            () => {
                window.dispatchEvent(new Event('resize'));
            }
            """
        )

        page.wait_for_timeout(1500)

        # ============================================================
        # SCROLL THROUGH ENTIRE PAGE
        # ============================================================
        # Helps ensure any dynamically rendered/lazy content is loaded.

        page.evaluate(
            """
            async () => {

                const delay = ms =>
                    new Promise(resolve => setTimeout(resolve, ms));

                const height = document.body.scrollHeight;

                window.scrollTo(0, height);

                await delay(500);

                window.scrollTo(0, 0);

                await delay(500);

            }
            """
        )

        # ============================================================
        # FINAL CONTENT CHECK
        # ============================================================

        page.wait_for_timeout(1000)

        # ============================================================
        # GENERATE PDF
        # ============================================================

        page.pdf(
            path=output_path,

            format="A4",

            print_background=True,

            prefer_css_page_size=False,

            margin={
                "top": "12mm",
                "right": "10mm",
                "bottom": "12mm",
                "left": "10mm"
            },

            display_header_footer=False
        )

        # ============================================================
        # CLOSE BROWSER
        # ============================================================

        browser.close()