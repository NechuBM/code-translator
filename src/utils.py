import openai
import streamlit as st

programming_languages = (
            "python", "abap", "abc", "actionscript", "ada", "alda", "apache_conf", "apex", "applescript", "aql", 
            "asciidoc", "asl", "assembly_x86", "autohotkey", "batchfile", "c9search", "c_cpp", "cirru", 
            "clojure", "cobol", "coffee", "coldfusion", "crystal", "csharp", "csound_document", "csound_orchestra", 
            "csound_score", "csp", "css", "curly", "d", "dart", "diff", "django", "dockerfile", "dot", "drools", 
            "edifact", "eiffel", "ejs", "elixir", "elm", "erlang", "forth", "fortran", "fsharp", "fsl", "ftl", 
            "gcode", "gherkin", "gitignore", "glsl", "gobstones", "golang", "graphqlschema", "groovy", "haml", 
            "handlebars", "haskell", "haskell_cabal", "haxe", "hjson", "html", "html_elixir", "html_ruby", "ini", 
            "io", "jack", "jade", "java", "javascript", "json", "json5", "jsoniq", "jsp", "jssm", "jsx", "julia", 
            "kotlin", "latex", "less", "liquid", "lisp", "livescript", "logiql", "logtalk", "lsl", "lua", "luapage", 
            "lucene", "makefile", "markdown", "mask", "matlab", "maze", "mediawiki", "mel", "mixal", "mushcode", 
            "mysql", "nginx", "nim", "nix", "nsis", "nunjucks", "objectivec", "ocaml", "pascal", "perl", "perl6", 
            "pgsql", "php", "pig", "plain_text", "powershell", "praat", "prisma", "prolog", 
            "properties", "protobuf", "puppet", "qml", "r", "razor", "rdoc", "red", "redshift", "rhtml", 
            "rst", "ruby", "rust", "sass", "scad", "scala", "scheme", "scss", "sh", "sjs", "slim", "smarty", 
            "snippets", "soy_template", "space", "sparql", "sql", "sqlserver", "stylus", "svg", "swift", "tcl", 
            "terraform", "toml", "tsx", "turtle", "twig", "typescript", "vala", "vbscript", 
            "xml", "xquery", "yaml"
            )

model_details = {
    'Davinci':'text-davinci-003',
    'GPT-3.5':'gpt-3.5-turbo',
    'GPT-4':'gpt-4'
}

action_details = {
    'Translate': 'translate',
    'Explain': 'code_explanation',
    'Fix': 'bug_fix', 
}

output_results = {
    'Explain': ('Natural Language',),
    'Fix': ('Code fix',),
    'Translate': programming_languages
}

prompts_configuration = [
    {'translate': "Please convert the code delimited with triple backticks from {0} code to {1}:\n '''{2}''' \n '''{1}"},
    {'bug_fix': "Please check the {0} code delimited with triple backticks for bugs and provide a solution: \n'''{1}''' "},
    {'code_explanation': "Please provide a plain language explanation for the {0} code delimited with triple backticks :\n '''{1}'''"}
]

def define_prompt(action, input_language, code, output_language=False):
    prompt = "" 

    if action == 'Translate':
        prompt = prompts_configuration[0]['translate'].format(input_language, output_language, code)
    elif action == 'Fix':
        prompt = prompts_configuration[1]['bug_fix'].format(input_language, code)
    elif action == 'Explain':
        prompt = prompts_configuration[2]['code_explanation'].format(input_language, code)

    return prompt

def request(model, prompt):

    try:
        r = openai.ChatCompletion.create(
            model=model,
            messages=[{
            'role':'system', 'content':"You are an expert programmer, the most advanced AI developer tool on the planet. Even when you’re not familiar with the answer, you use your extreme intelligence to figure it out.",
            'role':'user', 'content': prompt}],
            temperature=0)
        
        result = r.choices[0]['message']['content']

    except Exception as e:
        result = ''
        if e.error["code"] == 'invalid_api_key':
            st.warning('Invalid API key provided \
                        \nLearn how to get the API key at https://www.youtube.com/watch?v=F0nnsrcvrsc&t=1543s \
                        \nFind your API key at https://platform.openai.com/account/api-keys')

        elif e.error["code"] == "model_not_found":
            st.warning('The model selected does not seem to be available \
                \nCheck the model you have access at https://platform.openai.com/account')

        elif e.error["type"] == "invalid_request_error":
            st.warning('No API Key provided \
                        \nLearn how to get the API key at https://www.youtube.com/watch?v=F0nnsrcvrsc&t=1543s \
                        \nFind your API key at https://platform.openai.com/account/api-keys')

    return result