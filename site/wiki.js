// MkDocs' default search listens to keyup; input also supports paste and mobile keyboards.
document.addEventListener('DOMContentLoaded', function () {
  var originalSearch = window.doSearch;
  window.doSearch = function () {
    var query = document.getElementById('mkdocs-search-query').value
      .replace(/[^\p{L}\p{N}\s]/gu, ' ').replace(/\s+/g, ' ').trim();
    if (query.length > window.min_search_length) {
      if (window.Worker) window.searchWorker.postMessage({query: query});
      else window.displayResults(window.search(query));
    } else window.displayResults([]);
  };
  var originalInit = window.initSearch;
  if (originalInit) window.initSearch = function () {
    originalInit();
    var query = document.getElementById('mkdocs-search-query');
    if (query && query.value) window.doSearch();
  };
  var originalDisplay = window.displayResults;
  if (originalDisplay) window.displayResults = function (results) {
    var seen = new Set();
    originalDisplay(results.filter(function (result) {
      if (result.location.includes('#')) return false;
      var page = result.location;
      if (seen.has(page)) return false;
      seen.add(page);
      return true;
    }).slice(0, 50));
  };
  var input = document.getElementById('mkdocs-search-query');
  if (input) {
    if (originalSearch) input.removeEventListener('keyup', originalSearch);
    input.addEventListener('keyup', window.doSearch);
    input.addEventListener('input', window.doSearch);
  }
});
