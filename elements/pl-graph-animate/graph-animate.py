import networkx as nx
import pygraphviz as pgv
import numpy as np
import prairielearn as pl
import moviepy.editor as mpy
import warnings
import os
import tempfile
import lxml
import base64

# Default parameters
ENGINE_DEFAULT = "dot"
PARAMS_TYPE_DEFAULT = "adjacency-matrix"
DIRECTED_DEFAULT = "False"
DURATION_FRAME_DEFAULT = 2
ALGORITHM_DEFAULT = "dfs"
SHOW_STEPS_DEFAULT="True"
SHOW_WEIGHTS_DEFAULT="False"



def generate_frames_bfs_from_matrix(matrix, start_node, show_steps, show_weights,directed, size="5,5"):
    if isinstance(matrix, np.ndarray):  
        if directed=="True":
            G = nx.from_numpy_array(matrix, create_using=nx.DiGraph())  
        else:
            G = nx.from_numpy_array(matrix)
    else:
        G = matrix 
    A = nx.nx_agraph.to_agraph(G)

    bfs_edges = list(nx.bfs_edges(G, source=start_node)) 
    bfs_nodes = list(nx.bfs_tree(G, source=start_node).nodes) 

    frames = []

    for i in range(1, len(bfs_nodes) + 1):
        A_temp = A.copy()

        nodes_to_highlight = bfs_nodes[:i]
        for node in nodes_to_highlight:
            A_temp.get_node(node).attr['color'] = 'red'
            A_temp.get_node(node).attr['style'] = 'filled'
            A_temp.get_node(node).attr['fillcolor'] = 'red'

        edges_to_highlight = bfs_edges[:i-1]  
        for edge in edges_to_highlight:
            A_temp.get_edge(edge[0], edge[1]).attr['color'] = 'blue'
            A_temp.get_edge(edge[0], edge[1]).attr['penwidth'] = 2.5

        if show_steps=="True":
            A_temp.graph_attr['label'] = f"Step {i}: Current Node {bfs_nodes[i-1]} (BFS)"
            A_temp.graph_attr['labelloc'] = 'top'
        else:
            pass

        if show_weights=="True":
            for u, v, data in G.edges(data=True):
                weight = data.get('weight', 1.0)  
                A_temp.get_edge(u, v).attr['label'] = str(weight)
        else:
            pass
        A_temp.graph_attr['size'] = size
        A_temp.graph_attr['dpi'] = "300"

        # Save the graph to a temporary file
        temp_file = tempfile.NamedTemporaryFile(suffix=".png", delete=False)
        A_temp.draw(temp_file.name, format="png", prog="dot")

        frames.append(temp_file.name)

    return frames


def generate_frames_dfs_from_matrix(matrix, start_node, show_steps, show_weights, directed,size="5,5"):
    if isinstance(matrix, np.ndarray):  
        if directed=="True":
            G = nx.from_numpy_array(matrix, create_using=nx.DiGraph())  
        else:
            G = nx.from_numpy_array(matrix)
    else:
        G = matrix 


    A = nx.nx_agraph.to_agraph(G)

    # Get DFS traversal order
    dfs_edges = list(nx.dfs_edges(G, source=start_node))  # List of edges traversed in DFS
    dfs_nodes = list(nx.dfs_preorder_nodes(G, source=start_node))  # List of nodes in DFS order

    # List to store frames for the animation
    frames = []

    for i in range(1, len(dfs_nodes) + 1):
        A_temp = A.copy()
        # Highlight nodes in DFS order
        nodes_to_highlight = dfs_nodes[:i]
        for node in nodes_to_highlight:
            A_temp.get_node(node).attr['color'] = 'red'
            A_temp.get_node(node).attr['style'] = 'filled'
            A_temp.get_node(node).attr['fillcolor'] = 'red'

        # Highlight edges in DFS order
        edges_to_highlight = dfs_edges[:i-1] 
        for edge in edges_to_highlight:
            A_temp.get_edge(edge[0], edge[1]).attr['color'] = 'blue'
            A_temp.get_edge(edge[0], edge[1]).attr['penwidth'] = 2.5

        # Optionally set the graph title to indicate the current step and node
        if show_steps=="True":
            A_temp.graph_attr['label'] = f"Step {i}: Current Node {dfs_nodes[i-1]} (DFS)"
            A_temp.graph_attr['labelloc'] = 'top'
        else: 
            pass

        if show_weights=="True":
            for u, v, data in G.edges(data=True):
                weight = data.get('weight', 1.0)  # Default weight if not present
                A_temp.get_edge(u, v).attr['label'] = str(weight)
        else:
            pass

        # Set the size of the graph image
        A_temp.graph_attr['size'] = size
        A_temp.graph_attr['dpi'] = "300"

        # Save the graph to a temporary file
        temp_file = tempfile.NamedTemporaryFile(suffix=".png", delete=False)
        A_temp.draw(temp_file.name, format="png", prog="dot")

        frames.append(temp_file.name)

    return frames

def generate_frames_dijkstra_from_matrix(matrix, start_node, show_steps, show_weights,directed, size="5,5"):
    if isinstance(matrix, np.ndarray):
        if directed=="True":
            G = nx.from_numpy_array(matrix, create_using=nx.DiGraph())
        else:
            G = nx.from_numpy_array(matrix)
    else:
        G = matrix

    A = nx.nx_agraph.to_agraph(G)

    shortest_paths = nx.single_source_dijkstra_path_length(G, start_node)
    predecessors = nx.single_source_dijkstra_path(G, start_node)

    frames = []
    visited_nodes = set()
    visited_edges = set()

    step_count = 0  
    for target_node in shortest_paths.keys():
        step_count += 1
        if step_count % 2 != 0:  
            continue  
        A_temp = A.copy()
        path = predecessors[target_node]
        visited_nodes.update(path)
        for node in visited_nodes:
            A_temp.get_node(node).attr['color'] = 'red'
            A_temp.get_node(node).attr['style'] = 'filled'
            A_temp.get_node(node).attr['fillcolor'] = 'red'

        for i in range(len(path) - 1):
            edge = (path[i], path[i + 1])
            visited_edges.add(edge)
            A_temp.get_edge(edge[0], edge[1]).attr['color'] = 'blue'
            A_temp.get_edge(edge[0], edge[1]).attr['penwidth'] = 2.5

        if show_steps=="True":
            A_temp.graph_attr['label'] = f"Target Node {target_node}: Shortest Path (Dijkstra)"
            A_temp.graph_attr['labelloc'] = 'top'
        else:
            pass

        if show_weights=="True":
            for u, v, data in G.edges(data=True):
                weight = data.get('weight', 1.0)
                A_temp.get_edge(u, v).attr['label'] = str(weight)
        else:
            pass

        A_temp.graph_attr['size'] = size
        A_temp.graph_attr['dpi'] = "300"

        temp_file = tempfile.NamedTemporaryFile(suffix=".png", delete=False)
        A_temp.draw(temp_file.name, format="png", prog="dot")
        frames.append(temp_file.name)

    return frames

def create_graph_frame_dotty(dot_commands_dict,size="5,5"):
    frames = []
    for step, dot_command in dot_commands_dict.items():
        # Create a Pygraphviz AGraph object from the DOT command string
        A = pgv.AGraph(string=dot_command)
        A.graph_attr['size'] = size  
        A.graph_attr['dpi'] = "300"          
        temp_file = tempfile.NamedTemporaryFile(suffix=".png", delete=False)
        image_path = temp_file.name
        A.draw(image_path, format="png", prog="dot")  
        frames.append(image_path)
    return frames 



# Function to combine frames into a video
def create_video_from_frames(frames, output_file, frame_duration):
    clips = [mpy.ImageClip(f).set_duration(frame_duration) for f in frames]
    video = mpy.concatenate_videoclips(clips, method="compose")
    
    
    video.write_videofile(output_file, fps=24, verbose=False, logger=None)

def create_weighted_graph(matrix):
    G = nx.Graph()  
    size = matrix.shape[0]
    for i in range(size):
        for j in range(size):
            weight = matrix[i][j]
            if weight != 0 and weight != 100: 
                G.add_edge(chr(65 + i), chr(65 + j), weight=weight)  
    return G

def render(element_html: str, data: pl.QuestionData) -> str:
    # Parse the input parameters
    element = lxml.html.fragment_fromstring(element_html)
    input_param_name = pl.get_string_attrib(element, "params-name")
    input_type = pl.get_string_attrib(element, "params-type", PARAMS_TYPE_DEFAULT)
    algorithm = pl.get_string_attrib(element, "algorithm", ALGORITHM_DEFAULT).lower() 
    frame_duration = float(pl.get_string_attrib(element, "frame-duration", DURATION_FRAME_DEFAULT))
    show_steps = pl.get_string_attrib(element, "show-steps", SHOW_STEPS_DEFAULT)
    show_weights = pl.get_string_attrib(element, "show-weights", SHOW_WEIGHTS_DEFAULT)
    directed_graph=pl.get_string_attrib(element, "directed-graph", DIRECTED_DEFAULT)
    # Create video for input type adjacency-matrix
    if input_type==PARAMS_TYPE_DEFAULT:
        matrix = np.array(pl.from_json(data["params"][input_param_name]))
        

        start_node = 0  # Assuming traversal starts at node 0
        if algorithm == "dfs":

            frames=generate_frames_dfs_from_matrix(matrix, start_node,show_steps,show_weights,directed_graph)
        elif algorithm == "bfs":

            frames=generate_frames_bfs_from_matrix(matrix, start_node,show_steps,show_weights,directed_graph)
        elif algorithm == "dijkstra":

            frames=generate_frames_dijkstra_from_matrix(matrix, start_node,show_steps,show_weights,directed_graph)

        else:
            raise ValueError(f"Unsupported algorithm: {algorithm}")
    
    
    # Create video for input type dotty
    elif input_type=="dotty":
        dot_commands_dict = pl.from_json(data["params"][input_param_name])
        frames = create_graph_frame_dotty(dot_commands_dict)
        output_file = tempfile.NamedTemporaryFile(suffix=".mp4", delete=False).name
    
    
    
    
    # Save the video to a temporary file
    output_file = tempfile.NamedTemporaryFile(suffix=".mp4", delete=False).name
    create_video_from_frames(frames, output_file, frame_duration)

    # Read the video file and encode it in base64
    with open(output_file, "rb") as video_file:
        video_base64 = base64.b64encode(video_file.read()).decode('utf-8')

    
    return f'<video controls  width="100" height="100"><source src="data:video/mp4;base64,{video_base64}" type="video/mp4"></video>'
