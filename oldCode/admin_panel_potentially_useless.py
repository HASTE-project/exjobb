@app.route("/adminPanel")
def admin():
    return render_template("admin_panel.html")


# start a new test run and save score
# use timeit
# files = os.listdir(file_path)
# output: 1. text file with freq info 2. graphs showing performance

def admin_fun():
    #test max freq - kolla hur lång tid varje steg i for-loopen tar
    #test if set freq corresponds to actual freq
    #test freq for different image sizes

    # input: JSON file with test settings (possible to make multiple runs at once)
    json_file = request.form["file_path"]
    json_file = open(json_file, "r")
    run_information = json_file.read()
    run_information = json.loads(run_information)

    return run_information


@app.route("/adminPanel", methods=['POST'])


def test_timeit():
    runs = int(request.form["runs"])

    setup_template = '''
from simulator import admin_fun, get_files
run_information = admin_fun() 
frequency = run_information['run']['frequency']
color_channel = run_information['run']['color_channel']
binning = run_information['run']['binning']
file_path = run_information['run']['file_path']
connect_kafka = run_information['run']['connect_kafka']   
    '''

    for run in range(1, runs+1):
        setup = setup_template.replace("'run'", "'run{}'".format(run))
        save_results(str(timeit.timeit('get_files(file_path, frequency, binning, color_channel, connect_kafka)',
                                       setup=setup, number=3)), run)

    run_information = admin_fun()
    print(len(run_information))
    for run in run_information:
        frequency = run_information[run]['frequency']
        color_channel = run_information[run]['color_channel']
        binning = run_information[run]['binning']
        file_path = run_information[run]['file_path']
        connect_kafka = run_information[run]['connect_kafka']
        time_get_files(file_path, frequency, binning, color_channel, connect_kafka)
    return "test ready"


def save_results(results, run):
    fo = open("result.txt", "a")
    fo.write("Run nr, result: {} ".format(run))
    fo.write(results)
    fo.write("\n")
    fo.close()