/// <reference path="../macros/reviewable_file" />

$(function() {
    $('#files .file').each(function() {
        new r.macros.reviewable_file.ReviewableFile(this, $(this).attr('data-file-id'));
    });
});
