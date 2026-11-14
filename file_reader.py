def load_object(path, scale):
    faces = []
    vertices = []
    start_normals = [] # start with these then move to the real normals list
    normals = []
    with open(path) as file:
        for line in file:
            if line.startswith("v "):
                start = list(line.split())
                vertex = []
                for i in start:
                    if "." in i:
                        vertex.append(float(i))
                vertex[0] = vertex[0]*scale
                vertex[1] = -vertex[1]*scale
                vertex[2] = vertex[2]*scale
                vertices.append(vertex)
            if line.startswith("vn "):
                start = list(line.split())
                normal = []
                for i in start:
                    if "." in i:
                        normal.append(float(i))
                start_normals.append(normal)
            elif line.startswith("f "):
                start = list(line.split("//"))
                start[0]  = start[0].replace("f ", "")
                start[int(len(start)-1)] = start[int(len(start)-1)].replace("\n", "")
                if len(start) == 1: # triangle or quad with no //
                    face = start[0].split("/")
                    if len(face) == 1:
                        face = start[0].split(" ")
                        if len(face) == 3: # triangle
                            face[0] = int(face[0])
                            face[1] = int(face[1])
                            face[2] = int(face[2])
                            faces.append(face)
                        elif len(face) == 4: # quad
                            face2 = []
                            for y in face:
                                face2.append(y)
                            del face[1]
                            del face2[3]
                            face[0] = int(face[0])
                            face[1] = int(face[1])
                            face[2] = int(face[2])
                            face2[0] = int(face2[0])
                            face2[1] = int(face2[1])
                            face2[2] = int(face2[2])
                            faces.append(face)
                            faces.append(face2)
                    else:
                        if len(face) == 4: # triangle with v/vt
                            temp = face[1].split(" ")
                            del face[1]
                            for x in reversed(temp):
                                face.insert(1, x)
                            temp = face[3].split(" ")
                            del face[3]
                            for x in reversed(temp):
                                face.insert(3, x)
                            temp = face[5].split(" ")
                            del face[5]
                            for x in reversed(temp):
                                face.insert(5, x)
                            del face[1]
                            del face[2]
                            del face[3]
                            for x in range(len(face)):
                                face[x] = int(face[x])
                            faces.append(face)
                        if len(face) == 5: # quad with v/vt
                            temp = face[1].split(" ")
                            del face[1]
                            for x in reversed(temp):
                                face.insert(1, x)
                            temp = face[3].split(" ")
                            del face[3]
                            for x in reversed(temp):
                                face.insert(3, x)
                            temp = face[5].split(" ")
                            del face[5]
                            for x in reversed(temp):
                                face.insert(5, x)
                            temp = face[7].split(" ")
                            del face[7]
                            for x in reversed(temp):
                                face.insert(7, x)
                            del face[1]
                            del face[2]
                            del face[3]
                            del face[4]
                            for x in range(len(face)):
                                face[x] = int(face[x])
                            faces.append([face[0], face[1], face[2]])
                            faces.append([face[0], face[2], face[3]])
                        if len(face) == 7: # triangle with v/vt/vn
                            temp = face[2].split(" ")
                            del face[2]
                            for x in reversed(temp):
                                face.insert(2, x)
                            temp = face[5].split(" ")
                            del face[5]
                            for x in reversed(temp):
                                face.insert(5, x)
                            for x in range(len(face)):
                                face[x] = int(face[x])
                            x = (start_normals[face[2]-1][0]+start_normals[face[5]-1][0]+start_normals[face[8]-1][0])/3
                            y = (start_normals[face[2]-1][1]+start_normals[face[5]-1][1]+start_normals[face[8]-1][1])/3
                            z = (start_normals[face[2]-1][2]+start_normals[face[5]-1][2]+start_normals[face[8]-1][2])/3
                            normals.append([x, y, z])
                            del face[1]
                            del face[1]
                            del face[2]
                            del face[2]
                            del face[3]
                            del face[3]
                            for x in range(len(face)):
                                face[x] = int(face[x])
                            faces.append([face[0], face[1], face[2]])
                        if len(face) == 9: # quad with v/vt/vn
                            temp = face[2].split(" ")
                            del face[2]
                            for x in reversed(temp):
                                face.insert(2, x)
                            temp = face[5].split(" ")
                            del face[5]
                            for x in reversed(temp):
                                face.insert(5, x)
                            temp = face[8].split(" ")
                            del face[8]
                            for x in reversed(temp):
                                face.insert(8, x)
                            for x in range(len(face)):
                                face[x] = int(face[x])
                            x = (start_normals[face[2]-1][0]+start_normals[face[5]-1][0]+start_normals[face[8]-1][0])/3
                            y = (start_normals[face[2]-1][1]+start_normals[face[5]-1][1]+start_normals[face[8]-1][1])/3
                            z = (start_normals[face[2]-1][2]+start_normals[face[5]-1][2]+start_normals[face[8]-1][2])/3
                            x2 = (start_normals[face[2]-1][0]+start_normals[face[8]-1][0]+start_normals[face[11]-1][0])/3
                            y2 = (start_normals[face[2]-1][1]+start_normals[face[8]-1][1]+start_normals[face[11]-1][1])/3
                            z2 = (start_normals[face[2]-1][2]+start_normals[face[8]-1][2]+start_normals[face[11]-1][2])/3
                            normals.append([x, y, z])
                            normals.append([x2, y2, z2])
                            del face[1]
                            del face[1]
                            del face[2]
                            del face[2]
                            del face[3]
                            del face[3]
                            del face[4]
                            del face[4]
                            faces.append([face[0], face[1], face[2]])
                            faces.append([face[0], face[2], face[3]])
                        
                if len(start) == 4: # triangle with v//vn
                    temp = start[1]
                    del start[1]
                    temp2 = start[1]
                    del start[1]
                    temp = temp.split(" ")
                    for x in reversed(temp):
                        start.insert(1, x)
                    temp2 = temp2.split(" ")
                    for y in reversed(temp2):
                        start.insert(3, y)
                    face = []
                    for z in range(len(start)):
                        if not start[z] == " ":
                            face.append(int(start[z]))
                    x = (start_normals[face[1]-1][0]+start_normals[face[3]-1][0]+start_normals[face[5]-1][0])/3
                    y = (start_normals[face[1]-1][1]+start_normals[face[3]-1][1]+start_normals[face[5]-1][1])/3
                    z = (start_normals[face[1]-1][2]+start_normals[face[3]-1][2]+start_normals[face[5]-1][2])/3
                    normals.append([x, y, z])
                    del face[1]
                    del face[2]
                    del face[3]
                    faces.append(face)
                elif len(start) == 5: # quad with v//vn
                    temp = start[1]
                    del start[1]
                    temp2 = start[1]
                    del start[1]
                    temp3 = start[1]
                    del start[1]
                    temp = temp.split(" ")
                    for x in reversed(temp):
                        start.insert(1, x)
                    temp2 = temp2.split(" ")
                    for y in reversed(temp2):
                        start.insert(3, y)
                    temp3 = temp3.split(" ")
                    for z in reversed(temp3):
                        start.insert(5, z)
                    face = []
                    for a in range(len(start)):
                        face.append(int(start[a]))            
                    x = (start_normals[face[1]-1][0]+start_normals[face[3]-1][0]+start_normals[face[5]-1][0])/3
                    y = (start_normals[face[1]-1][1]+start_normals[face[3]-1][1]+start_normals[face[5]-1][1])/3
                    z = (start_normals[face[1]-1][2]+start_normals[face[3]-1][2]+start_normals[face[5]-1][2])/3
                    x2 = (start_normals[face[1]-1][0]+start_normals[face[5]-1][0]+start_normals[face[7]-1][0])/3
                    y2 = (start_normals[face[1]-1][1]+start_normals[face[5]-1][1]+start_normals[face[7]-1][1])/3
                    z2 = (start_normals[face[1]-1][2]+start_normals[face[5]-1][2]+start_normals[face[7]-1][2])/3
                    
                    normals.append([x, y, z])
                    normals.append([x2, y2, z2])
                    del face[1]
                    del face[2]
                    del face[3]
                    del face[4]
                    face2 = [] # i would make start2 = start but if i delete an item it deletes it from both bc of memory and pointers etc.
                    for b in face:
                        face2.append(b)
                    del face[1]
                    del face2[3]
                    faces.append(face)
                    faces.append(face2)
        triangles = []
        for face in faces:
            tri = []
            tri.append(vertices[face[0]-1])
            tri.append(vertices[face[1]-1])
            tri.append(vertices[face[2]-1])
            triangles.append(tri)
    return triangles, normals
