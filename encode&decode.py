from __future__ import with_statement
import base64
import binascii
from optparse import OptionParser
import os.path
import sys
import tkinter as tk
import tkinter.filedialog
import tkinter.messagebox


def convert(filename_in, filename_out, decode=False):

    with open(filename_in, 'rb') as f_in:
        if filename_out is None:
            f_out = sys.stdout
        else:
            f_out = open(filename_out, 'wb')
        func = base64.decode if decode else base64.encode
        try:
            func(f_in, f_out)
        except binascii.Error as errstr:
            print >> sys.stderr, errstr
        if filename_out is not None:
            f_out.close()


class GUI(tk.Tk):
    

    def __init__(self):
       
        tk.Tk.__init__(self)
        self.title('Base64 File Converter')

        
        self.filename_in = tk.StringVar()
        self.filename_out = tk.StringVar()
        self.decode = tk.BooleanVar()
        self.decode.set(False)

        
        for row, (label, var, cmd) in enumerate((
            ('Input', self.filename_in, self.get_in_filename),
            ('Output', self.filename_out, self.get_out_filename),
        )):
            tk.Label(self, text=label + ' File:') \
                .grid(row=row, column=0, sticky=tk.W)
            tk.Entry(self, textvariable=var) \
                .grid(row=row, column=1, sticky=tk.W + tk.E)
            tk.Button(self, text='Browse', command=cmd) \
                .grid(row=row, column=2)

        
        tk.Label(self, text='Mode:').grid(row=2, column=0, sticky=tk.W)
        modes = (('Encode', False), ('Decode', True))
        for row, (label, value) in enumerate(modes):
            tk.Radiobutton(self, text=label, variable=self.decode, value=value,
               anchor=tk.W).grid(row=(row + 2), column=1, sticky=tk.W)
        tk.Button(self, text='Convert', command=self.convert) \
            .grid(row=2, column=2, rowspan=2)

        self.columnconfigure(1, weight=1)
        self.rowconfigure(4, weight=1)

    def get_in_filename(self):
        
        self.filename_in.set(tk.filedialog.askopenfilename())

    def get_out_filename(self):
       
        self.filename_out.set(tk.filedialog.askopenfilename())

    def convert(self):
      
        if not self.filename_in.get():
            tkinter.messagebox.showerror('Error', 'Tidak ada file yang akan diinput')
            return
        if not self.filename_out.get():
            tkinter.messagebox.showerror('Error', 'Tidak ada file yang akan dioutput')
            return

        print ('%s from %s to %s ...' % (
            (self.decode.get() and 'Decoding' or 'Encoding'),
            os.path.basename(self.filename_in.get()),
            os.path.basename(self.filename_out.get())
        ))
        try:
            convert(self.filename_in.get(), self.filename_out.get(),
                self.decode.get())
            tkinter.messagebox.showinfo('Info', 'Conversion selesai.')
        except IOError as exc:
            tkinter.messagebox.showerror('Error', exc)


def main():
    parser = OptionParser()
    parser.add_option('-c', '--cli', dest='gui',
        action='store_false', help='use the command line interface (default)')
    parser.add_option('-d', '--decode', dest='decode',
        action='store_true', help='decode the data')
    parser.add_option('-e', '--encode', dest='decode',
        action='store_false', help='encode the data (default)')
    parser.add_option('-g', '--gui', dest='gui',
        action='store_true', help='use the user graphical interface')
    parser.add_option('-i', '--input', dest='input',
        metavar='FILE', help='input filename')
    parser.add_option('-o', '--output', dest='output',
        metavar='FILE', help='output filename')
    parser.set_defaults(decode=False, gui=False)

    opts, args = parser.parse_args()
    if opts.gui:
    
        GUI().mainloop()
        return

 

    if not opts.input:
        parser.error('Please specify an input filename.')
        parser.print_help()
        parser.exit()

    try:
        convert(opts.input, opts.output, opts.decode)
    except IOError as err:
        print >> sys.stderr, 'Error:', errstr

if __name__ == '__main__':
    main()