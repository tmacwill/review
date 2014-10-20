h = React.DOM

class Events
    @_map = {}

    @subscribe: (message, callback) ->
        if not (message of @_map)
            @_map[message] = []

        @_map[message].push(callback)

    @broadcast: (message, data) ->
        if not message in @_map
            return

        for callback in @_map[message]
            callback(data)

CommentBox = React.createClass
    render: ->
        h.div({className: 'comment-box'},
            h.h3({className: 'author'}, this.props.author)
            h.div({className: 'comment', contentEditable: 'true'}, this.props.comment)
        )

$ ->
    $commentsContainer = $('#comments-container')

    $('.linenodiv').each(->
        $(this).on('click', 'a', (e) ->
            # get the position of the line we're commenting on
            $this = $(this)
            top = $this.offset().top
            id = $this.parents('[data-file-id]').attr('data-file-id')

            # add a new container for the comment box
            $div = $('<div>')
            $commentsContainer.append($div)
            $div.offset({top: top})

            # render a comment box in the container
            React.renderComponent(
                CommentBox({
                    author: 'Tommy MacWilliam'
                    comment: ''
                }),
                $div[0]
            )

            $div.find('[contenteditable]').focus()

            return false
        )
    )
