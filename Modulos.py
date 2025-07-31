from tkinter import*
from tkinter import ttk
from tkinter import messagebox  
from tkcalendar import Calendar, DateEntry
import sqlite3

#pycep_correiros não existe mais e assim foi usado o brazilcep
#import pycep_correios
import brazilcep

#Bibliotecas para gerar relatórios em PDF
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, A4  #saída do PDF
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Image
import webbrowser