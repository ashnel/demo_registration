#select * from comments;

SELECT * FROM comments GROUP BY id ORDER BY comments.created_at DESC

#SELECT users.first_name, users.last_name, comments.comment, comments.message_id, comments.created_at FROM comments JOIN users on users.id = comments.user_id JOIN messages on messages.user_id = users.id