from pyglet.graphics.shader import Shader, ShaderProgram

# create vertex and fragment shader sources
vertex_source_default = """
#version 330
layout(location =0) in vec3 vertices;
layout(location =1) in vec4 colors;

out vec4 newColor;

// add a view-projection uniform and multiply it by the vertices
uniform mat4 view_proj;
uniform mat4 model;

void main()
{
    gl_Position = view_proj * model * vec4(vertices, 1.0f); // local->world->vp
    newColor = colors;
}
"""
vertex_source_phongtexN = """
#version 330
layout(location =0) in vec3 vertices;
layout(location =1) in vec2 texcoords;

out vec3 FragPosition;
out vec2 TexCoord;

// add a view-projection uniform and multiply it by the vertices
uniform mat4 view_proj;
uniform mat4 model;

void main()
{
    gl_Position = view_proj * model * vec4(vertices, 1.0f); // local->world->vp
    FragPosition = vec3(model * vec4(vertices, 1.0));
    TexCoord = texcoords;
}
"""
fragment_source_phongtexN ="""
#version 330 core

in vec3 FragPosition;
in vec2 TexCoord;
out vec4 FragColor;

uniform vec3 lightposition;
uniform vec3 viewposition;

uniform float I_intensity; // Intensity of the light source
uniform float I_ambient;   // Ambient intensity

uniform sampler2D base_color;
uniform sampler2D mixed_AO;
uniform sampler2D roughness;
uniform sampler2D specular;
uniform sampler2D nmal;

void main() {
    vec3 N = normalize(vec3(texture(nmal, TexCoord)));
    vec3 L = normalize(lightposition - FragPosition);
    vec3 V = normalize(viewposition - FragPosition);
    vec3 R = reflect(-L, N);

    float distance = length(lightposition - FragPosition);
    float distance2 = distance * distance; // distance squared

    // Ambient component
    vec3 ambient = I_ambient * (vec3(texture(mixed_AO, TexCoord)) * vec3(texture(base_color, TexCoord)));

    // Diffuse component
    float nl = max(dot(N, L), 0.0);
    vec3 diffuse = (nl * I_intensity / distance2) * vec3(texture(base_color, TexCoord));

    // Specular component
    float n = 1 / (0.1 * float(texture(roughness, TexCoord)) + 0.1);
    float rv = pow(max(dot(R, V), 0.0), n);
    vec3 specular = (rv * I_intensity / distance2) * vec3(texture(specular, TexCoord));

    // Final color calculation
    vec3 iout = ambient + diffuse + specular;
    vec3 bc = vec3(texture(base_color, TexCoord));
    FragColor = vec4(bc * iout, 1.0);
}

"""

fragment_source_default = """
#version 330
in vec4 newColor;

out vec4 outColor;

void main()
{
    outColor = newColor;
}
"""

fragment_source_phongtex ="""
#version 330 core

in vec3 FragPosition;
in vec3 vertexNormal;
in vec2 TexCoord;
out vec4 FragColor;

uniform vec3 lightposition;
uniform vec3 viewposition;

uniform float I_intensity; // Intensity of the light source
uniform float I_ambient;   // Ambient intensity

uniform sampler2D base_color;
uniform sampler2D mixed_AO;
uniform sampler2D roughness;
uniform sampler2D specular;

void main() {
    vec3 N = normalize(vertexNormal);
    vec3 L = normalize(lightposition - FragPosition);
    vec3 V = normalize(viewposition - FragPosition);
    vec3 R = reflect(-L, N);

    float distance = length(lightposition - FragPosition);
    float distance2 = distance * distance; // distance squared

    // Ambient component
    vec3 ambient = I_ambient * (vec3(texture(mixed_AO, TexCoord)) * vec3(texture(base_color, TexCoord)));

    // Diffuse component
    float nl = max(dot(N, L), 0.0);
    vec3 diffuse = (nl * I_intensity / distance2) * vec3(texture(base_color, TexCoord));

    // Specular component
    float n = 1 / (0.1 * float(texture(roughness, TexCoord)) + 0.1);
    float rv = pow(max(dot(R, V), 0.0), n);
    vec3 specular = (rv * I_intensity / distance2) * vec3(texture(specular, TexCoord));

    // Final color calculation
    vec3 iout = ambient + diffuse + specular;
    vec3 bc = vec3(texture(base_color, TexCoord));
    FragColor = vec4(bc * iout, 1.0);
}

"""
vertex_source_phongtex = """
#version 330
layout(location =0) in vec3 vertices;
layout(location =1) in vec3 nmal;
layout(location =2) in vec2 texcoords;

out vec3 vertexNormal;
out vec3 FragPosition;
out vec2 TexCoord;

// add a view-projection uniform and multiply it by the vertices
uniform mat4 view_proj;
uniform mat4 model;

void main()
{
    gl_Position = view_proj * model * vec4(vertices, 1.0f); // local->world->vp
    vertexNormal = nmal;
    FragPosition = vec3(model * vec4(vertices, 1.0));
    TexCoord = texcoords;
}
"""

vertex_source_phong = """
#version 330
layout(location =0) in vec3 vertices;
layout(location =1) in vec4 colors;
layout(location =2) in vec3 nmal;

out vec4 newColor;
out vec3 vertexNormal;
out vec3 FragPosition;

// add a view-projection uniform and multiply it by the vertices
uniform mat4 view_proj;
uniform mat4 model;

void main()
{
    gl_Position = view_proj * model * vec4(vertices, 1.0f); // local->world->vp
    newColor = colors;
    vertexNormal = nmal;
    FragPosition = vec3(model * vec4(vertices, 1.0));

}
"""
fragment_source_phong = """
#version 330 core

in vec3 FragPosition;
in vec3 vertexNormal;
in vec4 newColor;
out vec4 FragColor;

uniform vec3 K_a;  // Ambient reflectivity
uniform vec3 K_d;  // Diffuse reflectivity
uniform vec3 K_s;  // Specular reflectivity

uniform vec3 lightposition;
uniform vec3 viewposition;

uniform float I_intensity; // Intensity of the light source
uniform float I_ambient;   // Ambient intensity
uniform int shineness;     // Shininess factor for specular highlight

void main() {
    vec3 N = normalize(vertexNormal);
    vec3 L = normalize(lightposition - FragPosition);
    vec3 V = normalize(viewposition - FragPosition);
    vec3 R = reflect(-L, N);

    float distance = length(lightposition - FragPosition);
    float distance2 = distance * distance; // distance squared

    // Ambient component
    vec3 ambient = K_a * I_ambient;

    // Diffuse component
    float nl = max(dot(N, L), 0.0);
    vec3 diffuse = K_d * nl * I_intensity / distance2;

    // Specular component
    float rv = pow(max(dot(R, V), 0.0), shineness);
    vec3 specular = K_s * rv * I_intensity / distance2;

    // Final color calculation
    vec3 iout = ambient + diffuse + specular;
    FragColor = vec4(newColor.rgb * iout, newColor.a);
}

"""

vertex_source_gourang = """
#version 330
layout(location =0) in vec3 vertices;
layout(location =1) in vec4 colors;
layout(location =2) in vec3 nmal;

out vec4 newColor;
out vec3 vertexNormal;
out vec3 FragPosition;

uniform vec3 K_a;  // Ambient reflectivity
uniform vec3 K_d;  // Diffuse reflectivity
uniform vec3 K_s;  // Specular reflectivity

uniform vec3 lightposition;
uniform vec3 viewposition;

uniform float I_intensity; // Intensity of the light source
uniform float I_ambient;   // Ambient intensity
uniform int shineness;     // Shininess factor for specular highlight

// add a view-projection uniform and multiply it by the vertices
uniform mat4 view_proj;
uniform mat4 model;

void main()
{
    vec3 N = normalize(nmal);
    vec3 L = normalize(lightposition - vertices);
    vec3 V = normalize(viewposition - vertices);
    vec3 R = reflect(-L, N);

    float distance = length(lightposition - vertices);
    float distance2 = distance * distance; // distance squared

    // Ambient component
    vec3 ambient = K_a * I_ambient;

    // Diffuse component
    float nl = max(dot(N, L), 0.0);
    vec3 diffuse = K_d * nl * I_intensity / distance2;

    // Specular component
    float rv = pow(max(dot(R, V), 0.0), shineness);
    vec3 specular = K_s * rv * I_intensity / distance2;

    // Final color calculation
    vec3 iout = ambient + diffuse + specular;
    newColor = vec4(colors.rgb * iout, colors.a);

    gl_Position = view_proj * model * vec4(vertices, 1.0f); // local->world->vp

}
"""
fragment_source_gourang = """
#version 330 core

in vec4 newColor;
out vec4 FragColor;

void main() {
    FragColor = newColor;
}

"""

def create_program(vs_source, fs_source):
    # compile the vertex and fragment sources to a shader program
    vert_shader = Shader(vs_source, 'vertex')
    frag_shader = Shader(fs_source, 'fragment')
    return ShaderProgram(vert_shader, frag_shader)