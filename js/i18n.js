/* ── Bilingual UI runtime (English / العربية) ───────────
   Mirrors the accessibility pattern (js/a11y.js): the chosen
   language persists in localStorage under "lifta-lang" and is
   shared across both pages.

   Rendering is capture-based. The English site is the source
   of truth: on first apply, each translatable element's
   original text/markup/attribute is captured, and English
   always restores that captured value. Only Arabic is drawn
   from the dictionary (js/data/i18n.js), so this layer can
   never alter the English site, even if a dictionary "en"
   string drifts.

   On the map, map.js's setLang() wraps applyLang() so the one
   language control also swaps the basemap tile labels. Pages
   may set window.onLangChange(lang) to refresh dynamic content
   (e.g. re-render an open photo narrative in the new language).
   ─────────────────────────────────────────────────────── */

var LANG_KEY = 'lifta-lang';
var siteLang = 'en';

(function () {
  try {
    var s = localStorage.getItem(LANG_KEY);
    if (s === 'ar' || s === 'en') siteLang = s;
  } catch (e) {}
  // Set direction/lang immediately (the inline <head> script may have
  // already done this to avoid a flash; setting again is harmless).
  document.documentElement.setAttribute('lang', siteLang);
  document.documentElement.setAttribute('dir', siteLang === 'ar' ? 'rtl' : 'ltr');
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', function () { applyI18N(); syncLangButtons(); });
  } else {
    applyI18N();
    syncLangButtons();
  }
})();

/* Arabic string for a key, or null if absent (→ keep English). */
function _ar(key) {
  var e = (typeof siteI18N !== 'undefined') ? siteI18N[key] : null;
  return (e && e.ar) ? e.ar : null;
}

/* Apply the current language across the DOM. English restores the
   captured original; Arabic uses the dictionary (falling back to the
   original when no translation exists). */
function applyI18N() {
  var ar = (siteLang === 'ar');

  document.querySelectorAll('[data-i18n]').forEach(function (el) {
    if (el._i18nText == null) el._i18nText = el.textContent;
    var v = ar ? _ar(el.getAttribute('data-i18n')) : null;
    el.textContent = (v != null) ? v : el._i18nText;
  });

  document.querySelectorAll('[data-i18n-html]').forEach(function (el) {
    if (el._i18nHTML == null) el._i18nHTML = el.innerHTML;
    var v = ar ? _ar(el.getAttribute('data-i18n-html')) : null;
    el.innerHTML = (v != null) ? v : el._i18nHTML;
  });

  ['title', 'placeholder', 'aria-label'].forEach(function (attr) {
    var store = '_i18nAttr_' + attr;
    document.querySelectorAll('[data-i18n-' + attr + ']').forEach(function (el) {
      if (el[store] == null) el[store] = el.getAttribute(attr) || '';
      var v = ar ? _ar(el.getAttribute('data-i18n-' + attr)) : null;
      el.setAttribute(attr, (v != null) ? v : el[store]);
    });
  });
}

/* Reflect the active language on any language toggle buttons. */
function syncLangButtons() {
  document.querySelectorAll('[data-lang-btn]').forEach(function (b) {
    var on = b.getAttribute('data-lang-btn') === siteLang;
    b.classList.toggle('active', on);
    b.setAttribute('aria-pressed', String(on));
  });
}

/* Shared language switch: persistence + direction + chrome.
   The map's setLang() calls this in addition to swapping tiles;
   the gallery's toggle calls it directly. */
function applyLang(l) {
  if (l !== 'ar' && l !== 'en') return;
  siteLang = l;
  try { localStorage.setItem(LANG_KEY, l); } catch (e) {}
  document.documentElement.setAttribute('lang', l);
  document.documentElement.setAttribute('dir', l === 'ar' ? 'rtl' : 'ltr');
  applyI18N();
  syncLangButtons();
  if (typeof window.onLangChange === 'function') {
    try { window.onLangChange(l); } catch (e) {}
  }
}
