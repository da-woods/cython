from Cython.Compiler import Options
from Cython.Compiler import Pipeline
from Cython.Compiler import Errors
from Cython.Compiler import Main
from Cython.Compiler import Symtab
from Cython.Compiler import MemoryView
from Cython.Compiler.StringEncoding import EncodedString
from Cython.Compiler.Scanning import StringSourceDescriptor, FileSourceDescriptor

Errors.init_thread()
Errors.open_listing_file(None)
Options.use_shared_utility = True

options = Options.CompilationOptions()
context = Main.Context.from_options(options)
scope = Symtab.ModuleScope('MemoryView', parent_module = None, context = context, is_package=False)

import tempfile
import os
import shutil
with tempfile.TemporaryDirectory() as tmpdirname:
    pyx_file = os.path.join(tmpdirname, 'MemoryView.pyx')
    c_file = os.path.join(tmpdirname, 'MemoryView.c')
    with open(pyx_file, 'w'):
        pass
    source_desc = FileSourceDescriptor(pyx_file)
    comp_src = Main.CompilationSource(source_desc, EncodedString('MemoryView'), os.getcwd())
    result = Main.create_default_resultobj(comp_src, options)

    pipeline = Pipeline.create_shared_library_pipeline(context, scope, options, result)
    result = Pipeline.run_pipeline(pipeline, comp_src)
    shutil.copy(c_file, os.getcwd())
    print(result)
