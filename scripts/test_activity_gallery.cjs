/* Exercise the actual gallery component with a deterministic scroll container. */
const fs = require('node:fs');
const vm = require('node:vm');
const assert = require('node:assert/strict');
const path = require('node:path');
const source = fs.readFileSync(path.join(__dirname, '../static/js/activities.js'), 'utf8');
const tracks = [];
const sandbox = {window: {matchMedia: () => ({matches: false}), novaTrack: (...args) => tracks.push(args)},
  document: {addEventListener() {}}};
vm.runInNewContext(source, sandbox);
let scroll;
const gallery = sandbox.window.novaGallery();
gallery.$refs = {track: {children: new Array(6), clientWidth: 390, scrollLeft: 0,
  scrollTo(args) { scroll = args; this.scrollLeft = args.left; }}};
gallery.init();
assert.equal(gallery.count, 6);
gallery.go(1); assert.equal(gallery.current, 1); assert.equal(scroll.left, 390);
gallery.go(-1); assert.equal(gallery.current, 5); assert.equal(scroll.left, 1950);
gallery.go(6); assert.equal(gallery.current, 0);
gallery.go(3); assert.equal(gallery.current, 3);
gallery.$refs.track.scrollLeft = 780; gallery.sync(); assert.equal(gallery.current, 2);
sandbox.window.matchMedia = () => ({matches: true}); gallery.go(4); assert.equal(scroll.behavior, 'instant');
assert.equal(tracks[0][0], 'activity_gallery_interaction');
console.log('Gallery checks passed: next, previous, wrapping, thumbnail index, swipe synchronization, reduced motion and event context.');
