// MkDocs' default search listens to keyup; input also supports paste and mobile keyboards.
document.addEventListener('DOMContentLoaded', function () {
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
  if (input) input.addEventListener('input', function () {
    input.dispatchEvent(new Event('keyup'));
  });
});
