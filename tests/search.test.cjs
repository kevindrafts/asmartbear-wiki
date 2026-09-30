const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');
function search(query) {
  const sent = []; const shown = [];
  const input = {value:query,addEventListener(){}};
  const context = {Set,Event:class {}, document:{getElementById(){return input;},addEventListener(name, callback){this.ready=callback;}}, displayResults(r){shown.push(r);}, initSearch(){}, min_search_length:2, Worker:function(){}, searchWorker:{postMessage(m){sent.push(m);}}};
  context.window=context;
  vm.runInNewContext(fs.readFileSync('site/wiki.js','utf8'),context);
  context.document.ready();
  context.doSearch();
  return {sent,shown};
}
test('plain-language questions remove query punctuation',()=>{
  assert.equal(search('When should I hire?').sent[0].query,'When should I hire');
});
test('Unicode and business terms survive normalization',()=>{
  assert.equal(search('Cohen’s product–market fit?').sent[0].query,'Cohen s product market fit');
});
test('empty input clears results without querying',()=>{
  const result=search('???'); assert.equal(result.sent.length,0); assert.equal(result.shown.length,1);
});
