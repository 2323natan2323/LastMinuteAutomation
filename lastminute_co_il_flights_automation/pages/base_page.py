from playwright.sync_api import Page, Locator

class BasePage:
    def __init__(self, page: Page):
        self._page = page

        self._page.add_init_script("""
               const observer = new MutationObserver(() => {
                   const adIds = ['ZA_CAMP_DIV_1', 'ZA_CAMP_BG'];
                   adIds.forEach(id => {
                       const el = document.getElementById(id);
                       if (el) {
                           console.log('💣 Ad blocked before it rendered:', id);
                           el.remove();
                       }
                   });

                   const adClasses = ['.za_reset', '.overlay', '.ad-banner', '.popup', '.modal-backdrop'];
                   adClasses.forEach(cls => {
                       const els = document.querySelectorAll(cls);
                       els.forEach(el => {
                           console.log('💣 Ad element removed by class:', cls);
                           el.remove();
                       });
                   });
               });

               observer.observe(document.body, { childList: true, subtree: true });
           """)

    def click(self, locator):
        resolved_locator = self._resolve(locator)
        resolved_locator.wait_for(state="visible", timeout=5000)
        self._highlight_element(resolved_locator)
        resolved_locator.click()

    def safe_click(self, locator):
        resolved_locator = self._resolve(locator)
        resolved_locator.wait_for(state="visible", timeout=5000)
        self._page.wait_for_timeout(200)

        try:
            self._highlight_element(resolved_locator)
            resolved_locator.click(timeout=3000)
            print(f"✅ Safe click succeeded on {locator}")
        except Exception as e:
            print(f"⚠️ Regular click failed on {locator}: {str(e)}")
            print("🔧 Trying with force...")
            try:
                resolved_locator.click(force=True)
                print(f"✅ Force click succeeded on {locator}")
            except Exception as e2:
                print(f"❌ Even force click failed on {locator}: {str(e2)}")
                raise e2

    def fill_info(self, locator, text: str):
        resolved_locator = self._resolve(locator)
        resolved_locator.wait_for(state="visible", timeout=5000)
        resolved_locator.fill(text)

    def get_inner_text(self, locator) -> str:
        return self._resolve(locator).inner_text()

    def _highlight_element(self, locator: Locator, color: str = "yellow"):
        locator.evaluate(f"""
            (el) => {{
                const origShadow = el.style.boxShadow;
                const origBackground = el.style.backgroundColor;
                el.style.boxShadow = '0 0 10px 4px rgba(0, 150, 255, 0.7)';
                el.style.backgroundColor = '{color}';
                setTimeout(() => {{
                    el.style.boxShadow = origShadow;
                    el.style.backgroundColor = origBackground;
                }}, 300);
            }}
        """)

    def _remove_ad_popup_if_exists(self):
        """מזהה ומסיר פרסומות חוסמות מסך"""
        try:
            self._page.evaluate("""
                const adIds = ['ZA_CAMP_DIV_1', 'ZA_CAMP_BG'];
                adIds.forEach(id => {
                    const el = document.getElementById(id);
                    if (el) {
                        console.log('💥 Removing ad popup:', id);
                        el.remove();
                    }
                });

                const adClasses = ['.za_reset', '.overlay', '.ad-banner', '.popup', '.modal-backdrop'];
                adClasses.forEach(cls => {
                    const els = document.querySelectorAll(cls);
                    els.forEach(el => {
                        console.log('💥 Removing blocking class element:', cls);
                        el.remove();
                    });
                });
            """)
            print("🧹 Checked and removed ad popups if present")
        except Exception as e:
            print(f"⚠️ Failed to evaluate ad removal: {e}")

    def _resolve(self, locator) -> Locator:
        if isinstance(locator, str):
            return self._page.locator(locator)
        elif isinstance(locator, Locator):
            return locator
        else:
            raise TypeError(f"Unsupported locator type: {type(locator)}")

    def safe_landing(self):
        self._page.goto("https://lastminute.co.il")
        self._page.wait_for_load_state("networkidle")
        self._remove_ad_popup_if_exists()
