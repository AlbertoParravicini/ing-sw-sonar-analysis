from glob import glob
import re
import os

# RETRIEVE RAW FILES
raw_files = glob("logs/*/*RAW.txt")

for filepath in raw_files:

    new_file = ''
    build = "SUCCESS"
    with open(filepath) as fp:
        for line in fp:

            # REMOVE ANSI COLOR
            ansi_escape = re.compile(r'\x1B\[[0-?]*[ -/]*[@-~]')
            line = ansi_escape.sub('', line)

            # KEEP GOOD LINES
            if line.startswith("[INFO]") or line.startswith("[ERROR]") or line.startswith("[WARNING]"):
                new_file += line.replace('default_pom/~/', '')

                # CHECK FAILURES
                if line.endswith("BUILD FAILURE\n"):
                    build = "FAILURE"

    # CREATE THE LOG AND REMOVE THE RAW FILE
    with open(filepath.replace('RAW.txt', build + '.txt'), 'w') as f:
        f.write(new_file)

        os.remove(filepath)
