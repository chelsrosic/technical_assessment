import re

def check_file(filename: str) -> str: 
    '''
    Check open the input file if it is valid and and output information on it's contents

    Assumptions: 
    1) The input file name is a string, either a python file name or an invalid file name
    2) TODO will not be inside of block comments
    3) multi line comments can be more than one line in a row that each start with # 
       or one section that starts and ends with triple quotes
    4) TODO can be an ocothorp comment and (a multiline comment or a single line comment)
    5) a block/triple quote comment (that has been closed) followed by a comment starting with a # are considered two separate comments
    6) if there are more than one set of block/triple quote comments on one line that start/finish each other, 
        count it as more than one single comment line. i.e. the below is two single line comments: 
        ''' '''  ''' '''
    7) a line that is the beginning or ending of a multiline comment with a triple quote/block comments must only contain the triple quote or
        block code (+ whitespace) (I made this decision so block comments would not get mixed up with multiline strings)
    8) a line cannot contain both single line comments and multiline comments (i.e. in cases with triple quote block comments)
    9) the count for the total number of lines with comments only counts comments that start with a #
    '''
    def check_file_name(filename: str) -> bool:
        '''
        See if filename is valid. Filename is valid if it is a Python file
        '''
        if filename == '' or filename[0] == '.' or re.search('.py$', filename) is None:
            return False
        return True

    def line_starts_octothorp(line: str) -> bool:
        '''
        Return True if the line starts with an octothorp, 
        else return False
        '''
        if line != '' and line[0] == '#':
            return True
        return False

    if not check_file_name(filename):
        raise Exception('Invalid filename')

    num_lines = 0
    num_octothorp_comments = 0
    num_single_line_comments = 0
    num_lines_multiline_comments = 0 
    num_multiline_comments = 0 
    num_todos = 0
    in_block_comment = False

    with open(filename, 'r') as f:

        lines = f.readlines()
        strip_lines = lambda x: x.strip()
        lines = list(map(strip_lines, lines))

        for i in range(0, len(lines)):
            line = lines[i]
            num_lines +=1

            if in_block_comment:
                num_lines_multiline_comments +=1

            if re.search("^'''", line):

                # if the line has a number of triple quotes that are a 
                # multiple of two (i.e. it will end one comment and start another) 
                # you are not inside of a block comment because 
                # it is assumed that you cannot have multi line and single line comments on the same line 
                # a block/triple quote multiline comment starts and ends on lines that only contain ''' 
                if len(re.findall("'''", line)) > 1 and len(re.findall("'''", line))%2 == 0 and in_block_comment == False:
                    num_single_line_comments += int(len(re.findall("'''", line))/2)

                elif in_block_comment == False and re.search("'''$", line):
                    in_block_comment = True
                    num_lines_multiline_comments += 1
                    num_multiline_comments += 1

                else:
                    in_block_comment = False

            elif re.search('#', line) and in_block_comment == False:
                num_octothorp_comments += 1

                
                if line_starts_octothorp(line):

                    if line_starts_octothorp(line) and line[0:] != '#' and re.search('^TODO:', line[1:].strip()):
                        num_todos += 1

                    # see if comment is a multi line 
                    if (i-1 >= 0 and line_starts_octothorp(lines[i-1])) or (i+1 <= len(lines)-1 and line_starts_octothorp(lines[i+1])):

                        # see if this is the beginning of a multiline comment
                        if ((i-1 >= 0 and not line_starts_octothorp(lines[i-1])) or i-1 < 0) and (i+1 <= len(lines)-1 and line_starts_octothorp(lines[i+1])):
                            num_multiline_comments += 1    

                        num_lines_multiline_comments += 1
                        
                    else:
                        num_single_line_comments += 1

    return '''Number of lines in the file: {}, 
            Number of lines with (octothorp) comments: {}, 
            Number of single line comments: {}, 
            Number of TODOs: {}, 
            Number of multiline comments: {}, 
            Number of lines with multiline comments: {}'''.format(num_lines, num_octothorp_comments, num_single_line_comments, num_todos, num_multiline_comments, num_lines_multiline_comments)
    

if __name__ == "__main__":
    print(check_file('test.py'))
