/* Accessible navigation, sortable/searchable tables and file feedback. */
'use strict';
document.addEventListener('DOMContentLoaded', () => {
  const toggle = document.querySelector('#sidebar-toggle');
  toggle?.addEventListener('click', () => {
    const collapsed = document.body.classList.toggle('sidebar-collapsed');
    toggle.setAttribute('aria-expanded', String(!collapsed));
  });
  if (matchMedia('(max-width: 760px)').matches) {
    document.body.classList.add('sidebar-collapsed');
    toggle?.setAttribute('aria-expanded', 'false');
  }
  document.querySelectorAll('.dismiss').forEach(button => button.addEventListener('click', () => button.parentElement.remove()));
  document.querySelectorAll('.table-search').forEach(input => input.addEventListener('input', () => {
    const table = document.getElementById(input.dataset.table);
    if (!table) return;
    const query = input.value.toLocaleLowerCase('es').trim();
    let visible = 0;
    table.querySelectorAll('tbody tr').forEach(row => {
      row.hidden = !row.textContent.toLocaleLowerCase('es').includes(query);
      if (!row.hidden) visible++;
    });
    const empty = table.parentElement.querySelector('.search-empty');
    if (empty) empty.hidden = visible > 0;
  }));
  document.querySelectorAll('[data-sort]').forEach(button => button.addEventListener('click', () => {
    const table = button.closest('table');
    const body = table.tBodies[0];
    const index = Number(button.dataset.sort);
    const ascending = button.dataset.direction !== 'asc';
    table.querySelectorAll('th').forEach(th => th.removeAttribute('aria-sort'));
    button.closest('th').setAttribute('aria-sort', ascending ? 'ascending' : 'descending');
    button.dataset.direction = ascending ? 'asc' : 'desc';
    const rows = Array.from(body.rows);
    rows.sort((a,b) => a.cells[index].textContent.trim().localeCompare(b.cells[index].textContent.trim(), 'es', {numeric:true}) * (ascending ? 1 : -1));
    rows.forEach(row => body.appendChild(row));
  }));
  const input = document.querySelector('#archivo');
  const drop = document.querySelector('#drop-zone');
  const error = document.querySelector('#upload-error');
  const updateFile = () => {
    const file = input?.files[0];
    if (!file) return true;
    document.querySelector('#file-status').textContent = file.name + ' · ' + (file.size / 1024).toFixed(1) + ' KB';
    const invalid = !file.name.toLowerCase().endsWith('.csv') || file.size > 2 * 1024 * 1024;
    error.hidden = !invalid;
    error.textContent = invalid ? 'Selecciona un CSV de hasta 2 MB.' : '';
    return !invalid;
  };
  input?.addEventListener('change', updateFile);
  if (drop) {
    ['dragenter','dragover'].forEach(name => drop.addEventListener(name, event => {event.preventDefault();drop.classList.add('dragging');}));
    ['dragleave','drop'].forEach(name => drop.addEventListener(name, event => {event.preventDefault();drop.classList.remove('dragging');}));
    drop.addEventListener('drop', event => {
      if (event.dataTransfer.files.length) {
        input.files = event.dataTransfer.files;
        updateFile();
      }
    });
  }
  document.querySelectorAll('form[method="post"]').forEach(form => form.addEventListener('submit', event => {
    if (form.id === 'upload-form' && !updateFile()) {event.preventDefault();return;}
    form.setAttribute('aria-busy','true');
    const button = form.querySelector('button[type="submit"]');
    if (button) {button.disabled = true;button.textContent = form.id === 'upload-form' ? 'Analizando archivo…' : 'Procesando lote…';}
  }));
  if (document.querySelector('#preview')) document.querySelector('#preview').scrollIntoView({behavior:'smooth',block:'start'});
});
