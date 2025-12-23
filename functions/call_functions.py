from functions import get_files_info as gfi
from functions import get_file_content as gfc
from functions import write_file as wf
from functions import run_python_file as rpf
from google.genai import types

available_functions = types.Tool(
    function_declarations=[
        gfi.schema_get_files_info,
        gfc.schema_get_file_content,
        wf.schema_write_file,
        rpf.schema_run_python_file,
    ],
)


def call_functions(function_call, verbose=False):
    function_name, function_args = function_call.name, function_call.args
    if verbose:
        print(f"Calling function: {function_name}({function_args})")
    print(f"  - Calling function: {function_name}")
    function_map = {
        "get_files_info": gfi.get_files_info,
        "get_file_content": gfc.get_file_content,
        "write_file": wf.write_file,
        "run_python_file": rpf.run_python_file,
    }
    if function_name is None or not function_name or function_name not in function_map:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": f"Unknown function: {function_name}"},
                )
            ],
        )
    function_to_call = function_map[function_name]
    args = dict(function_args) if function_args else {}
    args["working_directory"] = "./calculator"
    function_result = function_to_call(**args)
    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_name,
                response={"result": function_result},
            )
        ],
    )
