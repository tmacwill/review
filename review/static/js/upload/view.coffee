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
            h.h4({className: 'timestamp'}, this.props.timestamp)
            h.div({className: 'comment'}, this.props.comment)
        )

$ ->
    React.renderComponent(
        CommentBox({
            author: 'Tommy MacWilliam'
            timestamp: '3 hours ago'
            comment: 'this looks okay, but have you considered using a pre-processor macro here?'
        }), $('#test')[0])
