/* 浮动导航手风琴 JS */
function toggleFloatNav() {
  document.getElementById('floatNav').classList.toggle('open');
}
function toggleSection(btn) {
  var items = btn.nextElementSibling;
  var isOpen = btn.classList.contains('open');
  document.querySelectorAll('.float-nav-section-btn').forEach(function(b) { b.classList.remove('open'); });
  document.querySelectorAll('.float-nav-items').forEach(function(i) { i.classList.remove('open'); });
  if (!isOpen) { btn.classList.add('open'); items.classList.add('open'); }
}
document.addEventListener('click', function(e) {
  var nav = document.getElementById('floatNav');
  if (!nav.contains(e.target)) nav.classList.remove('open');
});