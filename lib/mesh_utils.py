def loadMeshFile(filepath:str) -> list[list]:
    triangles = []
    with open(filepath, 'r') as f:
        triangle = []
        for line in f:
            line = line.replace('\n','') # remove any line breaks
            if line.startswith('Triangle') or len(line) < 1: # Start of a new triangle
                triangle = []
            else: # Add vertex to current triangle
                values = line.strip().replace(" ", "").split(',')
                x, y, z = map(float, line.strip().split(','))
                triangle.append((x, y, z))
                if len(triangle) == 3: # Triangle is complete, add it to the list
                    triangles.append(triangle)
    return triangles


    