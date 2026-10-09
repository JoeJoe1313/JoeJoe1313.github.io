(function () {
    'use strict';

    var search = document.getElementById('tech-notes-search');
    if (!search) {
        return;
    }

    var notes = Array.prototype.slice.call(document.querySelectorAll('.tech-note-preview'));
    var count = document.querySelector('.tech-notes-count');
    var empty = document.querySelector('.tech-notes-empty');

    function filterNotes() {
        var query = search.value.trim().toLowerCase();
        var visible = 0;
        notes.forEach(function (note) {
            note.hidden = note.textContent.toLowerCase().indexOf(query) === -1;
            if (!note.hidden) {
                visible += 1;
            }
        });
        count.textContent = visible + (visible === 1 ? ' note' : ' notes');
        empty.hidden = visible !== 0;
    }

    document.querySelector('.tech-notes-search').hidden = false;
    search.addEventListener('input', filterNotes);
    window.addEventListener('pageshow', filterNotes);
    filterNotes();
}());
