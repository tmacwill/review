/// <reference path="../macros/reviewable_file" />
/// <reference path="../macros/reviewers_filter" />

$(function() {
    var filter = new r.macros.reviewers_filter.ReviewersFilter($('#reviewers-filter'));
    $('#files .file').each(function() {
        new r.macros.reviewable_file.ReviewableFile(this, $(this).attr('data-file-id'));
    });
});
