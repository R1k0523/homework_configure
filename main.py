import io
import xml.etree.ElementTree as ElTree
import zipfile
import webbrowser
import re
from urllib.request import urlopen


def load(url):
    with urlopen(url) as f:
        data = f.read()
    return data

def get_package_url(name):
    data = load("https://pypi.org/simple/%s/" %name)
    root = ElTree.fromstring(data)
    package_url = None
    for elem in root[1]:
        if elem.tag == "a":
            url = elem.attrib["href"]
            if ".whl#" in url:
                package_url = url
    return package_url


def get_package_deps(url):
    deps = []
    data = load(url)
    obj = io.BytesIO(data)
    zipf = zipfile.ZipFile(obj)
    meta_path = [s for s in zipf.namelist() if "METADATA" in s][0]
    with zipf.open(meta_path) as f:
        meta = f.read().decode("utf-8")
    for line in meta.split("\n"):
        line = line.replace(";", " ").split()
        if not line:
            break
        if line[0] == "Requires-Dist:":
            if (len(re.findall('\[|]', line[1]))>0):
                line[1] = re.split('\[|]', line[1])[1]
            deps.append(line[1])
    return deps

def get_pypi_graph(name):
    graph = {}
    def rec(name):
        print(name)
        graph[name] = set()
        url = get_package_url(name)
        if not url:
            return
        deps = get_package_deps(url)
        for d in deps:
            graph[name].add(d)
            if d not in graph:
                rec(d)
    rec(name)
    return graph


def gv(graph):
    lines = "digraph{"
    for v1 in graph:
        for v2 in graph[v1]:
            if not v1 == v2:
                v1 = v1.replace('-', '_').replace('.', ',') #graphviz ругается на тире и точки
                v2 = v2.replace('-', '_').replace('.', ',')
                lines += '%s->%s;' % (v1, v2)
    lines += "}"
    return lines

def get_graph(name):
    graph = get_pypi_graph(name)
    print(gv_text(graph))
    digraph = gv(graph)
    if len(graph) > 1:
        url = "https://quickchart.io/graphviz?graph=" +digraph #можно использовать https://dreampuf.github.io/GraphvizOnline
        webbrowser.open(url, new=2)

def gv_text(graph):
    lines = ["digraph{"]
    for v1 in graph:
        for v2 in graph[v1]:
            if not v1 == v2:
                v1 = v1.replace('-', '_').replace('.', ',') #graphviz ругается на тире и точки
                v2 = v2.replace('-', '_').replace('.', ',')
                lines.append('%s->%s;' % (v1, v2))
    lines.append("}")
    return ("\n").join(lines)


get_graph("django")


