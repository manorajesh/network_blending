import bpy
import socket
import threading

scene = bpy.context.scene
frame_counter = scene.frame_start
render_path = scene.render.filepath

def next_frame():
    global frame_counter
    global scene
    frame_counter += 1
    scene.frame_set(frame_counter)
    print(frame_counter)

def update_node(socket):
    global frame_counter
    next_frame()
    socket.send(frame_counter.encode())

def wait_for_frame_done(socket):
    global frame_counter
    global scene
    while frame_counter <= scene.frame_end:
        if socket.recv(1024) == b'frame_done':
            update_node(socket)

def render():
    global frame_counter
    global scene
    scene.render.filepath = (render_path + str(scene.frame_current).zfill(3))

    bpy.ops.render.render(
        'INVOKE_DEFAULT',
        animation=False,
        write_still=True,
    )

def main():
    # prep socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ip = socket.gethostbyname(socket.gethostname())
    port = 40674

    s.bind(('', port))
    s.listen(5)

    s.accept()
    s.send(b'Connected to host:' + ip.encode())

    # spawn thread for node updates
    t = threading.Thread(target=wait_for_frame_done, args=(s,))
    t.start()

    # start frame loop
    while frame_counter <= scene.frame_end:
        next_frame()
        render()

# init frame_counter and send begin frame signal

# have seperate thread that listens for frame done signals, and increments frame_counter

# when frame_counter == end_frame, send end signal