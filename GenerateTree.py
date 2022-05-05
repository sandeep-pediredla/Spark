import sys

div = '<div id="node_@@cnt@@" class="window hidden" data-id="@@cnt@@" data-parent="data_parent" data-first-child="first_child" data-next-sibling="next_sibling"> <div class="tooltip">@@operation@@  <span class="tooltiptext">replace_hidden</span></div>  </div>'
op_filePath = sys.argv[2]
log_file = open(op_filePath, 'a')
op_str = ""
filepath = sys.argv[1]

class Node:
    def __init__(self, indented_line):
        self.children = []
        self.level = len(indented_line) - len(indented_line.lstrip())
        self.text = indented_line.strip()

    def add_children(self, nodes):
        childlevel = nodes[0].level
        while nodes:
            node = nodes.pop(0)
            if node.level == childlevel:  # add node as a child
                self.children.append(node)
            elif node.level > childlevel:  # add nodes as grandchildren of the last child
                nodes.insert(0, node)
                self.children[-1].add_children(nodes)
            elif node.level <= self.level:  # this node is a sibling, no more children
                nodes.insert(0, node)
                return

    def as_dict(self):
        if len(self.children) > 1:
            return {self.text: [node.as_dict() for node in self.children]}
        elif len(self.children) == 1:
            return {self.text: self.children[0].as_dict()}
        else:
            return self.text


def clean_qry(line):
    return int(line[line.index('[') + 1: line.index(']')]) - 1


def retrieveId(node):
    if node and node.text and node.text != "":
        return str(clean_qry(node.text))
    else:
        return ""


def getNextSibling(node, root):
    next_sibling = ""

    if root and len(root.children) > 1:
        found = False
        for child in root.children:
            if found:
                next_sibling = retrieveId(child)
            if child == node:
                found = True

    return next_sibling


def print_tree(node, root):
    global op_str
    line = (node.text)
    index = clean_qry(line)
    first_child = ""

    if len(node.children) > 0:
        first_child = retrieveId(node.children[0])

    next_sibling = getNextSibling(node, root)
    idx = line.index(']') + 2
    operation = line[idx: idx + 15]

    op_str += div.replace("@@cnt@@", str(index)).replace("@@operation@@", operation).replace("replace_hidden",
                                                                                             line).replace(
        "data_parent", retrieveId(root)).replace("next_sibling", str(next_sibling)).replace("first_child",
                                                                                            (first_child)) + '\n'

    for i in range(len(node.children)):
        if (i + 1) < (len(node.children)):
            print_tree(node.children[i], node)
        else:
            print_tree(node.children[i], node)


content_str = ""

with open(filepath) as fp:
    indented_text = fp.read()
    indented_text = indented_text.replace(":-", " ").replace(" : ", "   ")
fp.close()

first_ln = indented_text.partition('\n')[0]

root = Node(first_ln)
root.add_children([Node(line) for line in indented_text.splitlines()[1:] if line.strip()])
print_tree(root, None)

text_file = open("tree-view-visual-connections/demo/demo.html", "r")
from pathlib import Path

html_str = Path("tree-view-visual-connections/demo/demo.html").read_text()
text_file.close()
log_file.write(html_str.replace("@@@tree_view@@@", op_str))
log_file.close()
