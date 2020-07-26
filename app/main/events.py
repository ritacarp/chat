from flask import session, request
from flask_socketio import emit, join_room, leave_room
from app import socketio


@socketio.on('joined', namespace='/chat')
def joined(message):
    """Sent by clients when they enter a room.
    A status message is broadcast to all people in the room."""
    room = session.get('room')
    join_room(room)
    print(f"\n\n{session.get('name')} joined a room.  The session id is {request.sid}\n\n")
    #emit('status', {'msg': session.get('name') + ' has entered the room.'}, room=room)
    emit('status', {'thisUser': session.get('name'), 'sender': 'System', 'vClass': 'system', 'msg': session.get('name') + ' has entered room ' + room + '.'}, room=room)



@socketio.on('text', namespace='/chat')
def text(message):
    """Sent by a client when the user entered a new message.
    The message is sent to all people in the room."""
    
    # print(f"\n\nin route text: message = {message}, name={session.get('name')}, room = {session.get('room')}\n\n ")
    print(f"\n\n{session.get('name')} sent a message.  The session id is {request.sid}\n\n")
    
    room = session.get('room')
    #emit('message', {'msg': session.get('name') + ':' + message['msg']}, room=room)
    emit('message', {'sid': request.sid, 'thisUser': session.get('name'), 'msg': message['msg']}, room=room)


@socketio.on('left', namespace='/chat')
def left(message):
    """Sent by clients when they leave a room.
    A status message is broadcast to all people in the room."""
    who = session.get('name')
    room = session.get('room')
    leave_room(room)
    #emit('status', {'msg': session.get('name') + ' has left the room.'}, room=room)
    emit('status', {'thisUser': who, 'sender': 'System', 'vClass': 'system','msg': session.get('name') + ' has left room ' + room + '.'}, room=room)