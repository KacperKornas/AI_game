from pygame.math import Vector2
class Matrix:
    
    def identity():
        return [[1, 0, 0],
                [0, 1, 0],
                [0, 0, 1]]
        
    def multiply(m, n):
        mat_temp = [[0.0, 0.0, 0.0],
                [0.0, 0.0, 0.0],
                [0.0, 0.0, 0.0]]

        for i in range(3):
            for j in range(3):
                for k in range(3):
                    mat_temp[i][j] += m[i][k] * n[k][j]

        return mat_temp
    
    def rotate(fwd, side):
        mat_temp = [[fwd.x, fwd.y, 0],
                    [side.x, side.y, 0],
                    [0, 0, 1]]
        
        return Matrix.multiply(Matrix.identity(), mat_temp)
    
    def translate(mat, vec):
        mat_trans = [[1, 0, 0],
               [0, 1, 0],
               [vec.x, vec.y, 1]]
        
        return Matrix.multiply(mat, mat_trans)
    
    def transformVector2Ds(vPoint: Vector2, mat):
        tempX = (mat[0][0] * vPoint.x) + (mat[1][0] * vPoint.y) + (mat[2][0])
        tempY = (mat[0][1] * vPoint.x) + (mat[1][1] * vPoint.y) + (mat[2][1])
        return Vector2(tempX, tempY)
    
    def pointToLocalSpace(point: Vector2, agentHeading: Vector2, agentSide: Vector2, agentPosition: Vector2):
        Tx = -agentPosition.dot(agentHeading)
        Ty = -agentPosition.dot(agentSide)
        
        matrix = [[agentHeading.x, agentSide.x, 0],
                  [agentHeading.y, agentSide.y, 0],
                  [Tx, Ty, 0]]
        
        return Matrix.transformVector2Ds(point, matrix)
    
    def pointToWorldSpace(point: Vector2, agent_heading: Vector2, agent_side: Vector2, agent_pos: Vector2):
        matrix = Matrix.rotate(agent_heading, agent_side)
        matrix = Matrix.translate(matrix, agent_pos)
        
        return Matrix.transformVector2Ds(point, matrix)

    def VectorToWorldSpace(vec: Vector2, agentHeading: Vector2, agentSide: Vector2) -> Vector2:
        matrix = Matrix.rotate(agentHeading, agentSide)
        return Matrix.transformVector2Ds(vec, matrix)
        