import flask
from flask import request, jsonify,render_template
from var_dump import var_dump
from api.sudoku_solver.sudoku import SudoKu,Node,breadth_first_tree_search
app = flask.Flask(__name__)
print("Server Started!")


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.route('/', methods=['GET'])
def main():
    return render_template('index.html'),200

@app.route('/api/sudoku/', methods=['GET','POST'])
def sudoku_solver():
    print("Received POST Request!")
    print(request)
    response = dict()
    try:
        query_parameters = request.get_json()
        if len(query_parameters)!=1:
            print("Exeception 0")
            raise Exception(0) 
        sudoku = query_parameters["sudoku"]
        if sudoku is None:
            print("Exeception 1")
            raise Exception(1)
        if len(sudoku)!=9 or len(sudoku[0])!=9:
            print("Exeception 2")
            response["success"]=0
            response["error"]="Invalid Sudoku Format! Please refer the API Documentation."
            return jsonify(response)
        for i in range(9):
            for j in range(9):
                if type(sudoku[i][j]) != int:   
                    print("Exeception 3")                 
                    response["success"]=0
                    response["error"]="Invalid Sudoku Format! Please refer the API Documentation."
                    return jsonify(response)
                
                if sudoku[i][j]<0 and sudoku[i][j]>9:   
                    print("Exeception 4")                                    
                    response["success"]=0
                    response["error"]="Invalid Sudoku Format! Please refer the API Documentation."
                    return jsonify(response)
        
        sudoku_solve=SudoKu(sudoku)
        solved = breadth_first_tree_search(sudoku_solve)
        if solved is None:
            response["success"] = -1
            response["error"] = "Sudoku is not solvable!"
            return jsonify(response)
        
        response["success"] = 1
        response["solution"] = solved.state
        return jsonify(response)

    except:
        response["success"] = 0
        response["error"] = "Bad Request Format! Please refer the API Documentation."
        return jsonify(response)
    
    return "Yet to make."
if __name__ == '__main__':  
   app.run(debug = True)  