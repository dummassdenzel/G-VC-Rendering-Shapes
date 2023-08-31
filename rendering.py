import numpy as np
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader
import glfw

#shaders
vertex_src = """
#version 330 core

layout(location = 0) in vec3 position;
layout(location = 1) in vec3 color;

out vec3 v_color;

void main()
{
    gl_Position = vec4(position, 1.0);
    v_color = color;
}
"""

fragment_src = """
#version 330 core

in vec3 v_color;

out vec4 out_color;

void main()
{
    out_color = vec4(v_color, 1.0);
}
"""





#glfw window initialization
glfw.init()
window = glfw.create_window(800, 600, "My First Render", None, None)

if not window:
    glfw.terminate()
    exit()

glfw.make_context_current(window)



#local space/object creation
#vertices coordinates
vertices = [-0.5, -0.5, 0, 1.0, 0.0, 0.0,
            0.5, -0.5, 0, 0.0, 1.0, 0.0,
            0.5, 0.5, 0, 0.0, 0.0, 1.0,
            -0.5, 0.5, 0, 1.0, 0.0, 1.0]
vertices = np.array(vertices, dtype=np.float32)

#compile the shader
shader = compileProgram(compileShader(vertex_src, GL_VERTEX_SHADER), compileShader(fragment_src, GL_FRAGMENT_SHADER))

#sending/binding data to the gpu
#vbo
vbo = glGenBuffers(1)
glBindBuffer(GL_ARRAY_BUFFER,vbo)
glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)
#vertex
glEnableVertexAttribArray(0)
glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 24, ctypes.c_void_p(0)) 
#color
glEnableVertexAttribArray(1)
glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 24, ctypes.c_void_p(12))



# rendering loop

glUseProgram(shader)
glClearColor(0.1, 0.1, 0.1, 1)

while not glfw.window_should_close(window):
    glfw.poll_events()#get all events
    glClear(GL_COLOR_BUFFER_BIT)#set the buffer color set in theglClearColor function

    #render/display your objects here
    #function to draw array(MODE_OF_OBJECT_ASSESSMBLY, first vertex, number of vertices)
    glDrawArrays(GL_QUADS, 0, 4)

    #swap the next buffer
    glfw.swap_buffers(window)


#object deletion
glDeleteProgram(shader)
glDeleteBuffers(1, (vbo,))
glfw.terminate()
