import dash
import dash_html_components as html
import dash_core_components as dcc
import dash_table
import dash_table_experiments as dt
import base64
import glob
import datetime
import numpy as np
import os, errno
import pandas as pd
import subprocess

def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc:  # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise
#png_path = '/media/vishnu/htru_candidates/vishnu/ozstar_cands/latest_msp_candidates_div16_after_topo_60_percent/'
png_path = '/media/vishnu/htru_candidates/vishnu/ozstar_cands/latest_msp_candidates_div16_htru_retrained_topo_40_percent/'
#df = pd.read_csv('msp_search_candidates_above_50_percent_htru_retrained_28_jan.csv', index_col=False)
#df = pd.read_csv('msp_search_candidates_above_50_percent_htru_retrained_12_Apr_after_topo_60_percent.csv', index_col=False)
df = pd.read_csv('msp_search_candidates_above_70_percent_htru_retrained_17_Apr_topo_40_percent.csv', index_col=False)
df["Beam"] = df.Beam.map("{:02}".format)
df['Cand Name'] = df['pfd_name'].astype(str) + '.png' 
#split = df["pfd_name"].str.split("_", expand = True) 
#df['Spin Period Ms'] = 
df['Spin Period'] = df['Spin Period (ms)']/1000
df = df.loc[df['Sigma'] >= 8.0]
df1 = pd.read_csv('nearby_pulsars_htru_low_lat_pointings.csv', index_col=False)
df1["Beam"] = df1.Beam.map("{:02}".format)
app = dash.Dash()
all_png_files = glob.glob(png_path + "*.png")
user_classification = pd.DataFrame(columns=['UserName','TimeStamp', 'ImageName', 'Pointing', 'Beam', 'Classification'])
if not os.path.exists(png_path + 'selected/'):
    mkdir_p(png_path + 'selected/')

if not os.path.exists('user_classification_msp_cands_htru_retrained_after_topo_debacle.csv'):
    with open('user_classification_msp_cands_htru_retrained_after_topo_debacle.csv', 'w') as outfile:
        outfile.write('UserName' + ',' 'TimeStamp' + ',' + 'ImageName' + ',' + 'Pointing' + ',' + 'Beam' + ',' + 'DM-Frac' + ',' + 'Classification' + '\n')

pics_score = np.linspace(0,1,11)
'''
User Classification is as follows:

			0 = Noise (Default Selection if user does not click other buttons)
			1 = Pulsar (Known) 
			2 = Harmonic (of a known pulsar)
			3 = RFI
			4 = CLASS A candidate = Extremely likely to be a new discovery
			5 = Class B candidate = Less Promising but worth checking for followup processing 

													'''


df2 = pd.read_csv('user_classification_msp_cands_htru_retrained_after_topo_debacle.csv')

df3 = df.merge(df2, left_on = 'Cand Name', right_on = 'ImageName', how='left', indicator=True)

df4 = df3[df3["_merge"] == "left_only"].drop(columns=["_merge", "TimeStamp", "Classification", "Pointing_y", "Beam_y", "DM-Frac_y",  "UserName", "ImageName"])
df4.columns = df.columns
print('Total files available: ', len(df.index))
print(df.columns)
df = df4
print('Total files still to be inspected: ', len(df.index))
#df = df.loc[(df['Spin Period (ms)'] >= 1) & (df['Spin Period (ms)'] <= 100)]
#print('Total files: ', len(df.index))
existing_candidates = []
for index, row in df.iloc[0:].iterrows():
    image_filename = png_path + row['Cand Name']
    if os.path.isfile(image_filename):
        existing_candidates.append(True)
    else:
        existing_candidates.append(False)

df10 = df.loc[existing_candidates]
df = df10

print('Candidates with existing files: ', len(df.index))


#app.css.append_css({
#    'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css'
#})

# Boostrap CSS.
app.css.append_css({'external_url': 'https://codepen.io/amyoshino/pen/jzXypZ.css'})



colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}


app.layout = html.Div([
    html.Div(children=[
    html.H1(children='Pulsar Candidate Viewer', style={
            'textAlign': 'center',
            'color': colors['text']
        }),
    html.H5(children='By Vishnu Balakrishnan', style={
            'textAlign': 'right',
            'color': colors['text']
        }),

#html.Img(id = 'current-image', className='container', style={'maxWidth': '750px'}),

#html.Div([
dcc.RangeSlider(
    count=10,
    min=0,
    max=1,
    step=0.1,
    id='pics range',
    marks={i: 'PICS Score: {0:.1f}'.format(i) for i in pics_score},
    value=[0.5, 1.0])
]),
html.Div([
html.Div([

html.Img(id = 'current-image', style={'width': '59%'}),
], className="eight columns"),


html.Div([
html.H2(html.I('Nearby Known Pulsars'), style={'textAlign': 'center'}),
html.Div(dt.DataTable(
    rows=[{}], # initialise the rows
    row_selectable=True,
    filterable=True,
    sortable=True,
    selected_row_indices=[],
    id='nearby-pulsar-table'), style={'margin-left': -500, 'margin-right': 0, 'max-width': '3000px', 'overflow-x': 'scroll'}
   #id='nearby-pulsar-table'), style={'display': 'inline-block'}
),
], className="four columns")
], className="row"),
#]),
html.Div([
html.Div([
html.Button(id='pulsar-button', n_clicks_timestamp='0', children='Pulsar'),
html.Button(id='harmonic-button', n_clicks_timestamp='0', children='Harmonic'),
html.Button(id='rfi-button', n_clicks_timestamp='0', children='RFI'),
html.Button(id='class_a_candidate',  n_clicks_timestamp='0', children='ClassA'),
html.Button(id='class_b_candidate', n_clicks_timestamp='0', children='ClassB'),
html.Button(id='next-button', n_clicks = 0, n_clicks_timestamp='0', children='Next'),
html.Div(id='intermediate-classifications', style={'display': 'none'}),
html.Div(id='container')
], className="eight columns"),
#], className="row"),
#
html.Div([
html.Div([
html.H2(html.I('Harmonics'), style={'textAlign': 'center'}),
html.Div(id='container1')
], className="four columns"),
], className="row")

])
])

#app.layout = html.Div([
#    html.Div(children=[
#    html.H1(children='Pulsar Candidate Viewer', style={
#            'textAlign': 'center',
#            'color': colors['text']
#        }),
#    html.H5(children='By Vishnu Balakrishnan', style={
#            'textAlign': 'right',
#            'color': colors['text']
#        }),
#
##html.Img(id = 'current-image', className='container', style={'maxWidth': '750px'}),
#
##html.Div([
#dcc.RangeSlider(
#    count=10,
#    min=0,
#    max=1,
#    step=0.1,
#    id='pics range',
#    marks={i: 'PICS Score: {0:.1f}'.format(i) for i in pics_score},
#    value=[0.9, 1.0])
#]),
#html.Div([
#html.Div([
#
#html.Img(id = 'current-image', style={'width': '59%'}),
#], className="eight columns"),
#
#
#html.Div([
#html.H2(html.I('Nearby Known Pulsars'), style={'textAlign': 'center'}),
#html.Div(dt.DataTable(
#    rows=[{}], # initialise the rows
#    row_selectable=True,
#    filterable=True,
#    sortable=True,
#    selected_row_indices=[],
#    id='nearby-pulsar-table'), style={'margin-left': -500, 'margin-right': 0, 'max-width': '3000px', 'overflow-x': 'scroll'}
#   #id='nearby-pulsar-table'), style={'display': 'inline-block'}
#),
#], className="four columns")
#], className="row"),
##]),
#html.Div([
#html.Button(id='pulsar-button', n_clicks_timestamp='0', children='Pulsar'),
#html.Button(id='harmonic-button', n_clicks_timestamp='0', children='Harmonic'),
#html.Button(id='rfi-button', n_clicks_timestamp='0', children='RFI'),
#html.Button(id='class_a_candidate',  n_clicks_timestamp='0', children='ClassA'),
#html.Button(id='class_b_candidate', n_clicks_timestamp='0', children='ClassB'),
#html.Button(id='next-button', n_clicks = 0, n_clicks_timestamp='0', children='Next'),
#html.Div(id='intermediate-classifications', style={'display': 'none'}),
#html.Div(id='container')
#], className="eight columns"),
##
#])
#])
#html.Div([
#html.Div(id='ml_score1')
#], className="four columns"),
#], className="row"),
#])
#
#
#
@app.callback(dash.dependencies.Output('current-image', 'src'),
              [dash.dependencies.Input('pics range', 'value'),
               dash.dependencies.Input('next-button', 'n_clicks')])
def update_image_src(value, next_button):

    

    pics_score_min = value[0]
    pics_score_max = value[1]
    dff = df[(df['pics_score_htru'] >= pics_score_min) & (df['pics_score_htru'] <= pics_score_max)]
    dff = dff.reset_index()

    image_filename = png_path + dff['Cand Name'][next_button] # iterate over images 
    encoded_image = base64.b64encode(open(image_filename, 'rb').read())
    return 'data:image/png;base64,{}'.format(encoded_image.decode())





@app.callback(dash.dependencies.Output('next-button', 'n_clicks'),
              [dash.dependencies.Input('pics range', 'value')])
def reset_click_number(value):

    return None
#
#
@app.callback(dash.dependencies.Output('container', 'children'),
              [dash.dependencies.Input('pics range', 'value'),
               dash.dependencies.Input('pulsar-button', 'n_clicks_timestamp'),
               dash.dependencies.Input('harmonic-button', 'n_clicks_timestamp'),
               dash.dependencies.Input('rfi-button', 'n_clicks_timestamp'),
               dash.dependencies.Input('class_a_candidate', 'n_clicks_timestamp'),
               dash.dependencies.Input('class_b_candidate', 'n_clicks_timestamp'),
               dash.dependencies.Input('next-button', 'n_clicks'),
               dash.dependencies.Input('next-button', 'n_clicks_timestamp')])
def update_user_classification_on_screen(pics_value, pulsar_button, harmonic_button, rfi_button, class_a_button, class_b_button, n_clicks, next_button):

    msg = 'No Classifications Done Yet'

    pics_score_min = pics_value[0]
    pics_score_max = pics_value[1]
    dff = df[(df['pics_score_htru'] >= pics_score_min) & (df['pics_score_htru'] <= pics_score_max)]

    dff = dff.reset_index()
    if n_clicks > len(dff.index):
        msg = 'Congratulations! You are done with this beam!!'
        return html.Div([

        html.Div(msg)])
    else: 
        image_filename = dff['Cand Name'][n_clicks] # iterate over images
    
    
    
        if int(pulsar_button) > int(harmonic_button) and int(pulsar_button) > int(rfi_button) and int(pulsar_button) > int(next_button) and int(pulsar_button) > int(class_a_button) \
        and int(pulsar_button) > int(class_b_button):
    
            msg = '%s candidate is currently marked as a pulsar!!' %(image_filename)
 
        elif int(harmonic_button) > int(pulsar_button) and int(harmonic_button) > int(rfi_button) and int(harmonic_button) > int(next_button) and \
        int(harmonic_button) > int(class_a_button) and int(harmonic_button) > int(class_b_button):
    
            msg = '%s candidate is currently marked as a harmonic!!' %(image_filename)

        elif int(rfi_button) > int(pulsar_button) and int(rfi_button) > int(harmonic_button) and int(rfi_button) > int(next_button) and int(rfi_button) > int(class_a_button) and \
        int(rfi_button) > int(class_b_button):
    
            msg = '%s candidate is currently marked as RFI!!' %(image_filename)
    
        elif int(next_button) > int(pulsar_button) and int(next_button) > int(harmonic_button) and int(next_button) > int(rfi_button) and int(next_button) > int(class_a_button) and \
        int(next_button) > int(class_b_button):

            msg = '%s candidate is currently marked as Noise!!' %(image_filename)

        elif int(class_a_button) > int(pulsar_button) and int(class_a_button) > int(harmonic_button) and int(class_a_button) > int(rfi_button) and \
        int(class_a_button) > int(next_button)  and int(class_a_button) > int(class_b_button):

            msg = '%s candidate is currently marked as Class A candidate. Yay!!' %(image_filename)

        elif int(class_b_button) > int(pulsar_button) and int(class_b_button) > int(harmonic_button) and int(class_b_button) > int(rfi_button) and \
        int(class_b_button) > int(next_button) and int(class_b_button) > int(class_a_button):

            msg = '%s candidate is currently marked as Class B candidate.!!' %(image_filename)


        return html.Div([

        html.Div(msg)

        ], style={'color': 'black', 'fontSize': 18})

@app.callback(dash.dependencies.Output('intermediate-classifications', 'children'),
              [dash.dependencies.Input('pics range', 'value'),
               dash.dependencies.Input('pulsar-button', 'n_clicks_timestamp'),
               dash.dependencies.Input('harmonic-button', 'n_clicks_timestamp'),
               dash.dependencies.Input('rfi-button', 'n_clicks_timestamp'),
               dash.dependencies.Input('class_a_candidate', 'n_clicks_timestamp'),
               dash.dependencies.Input('class_b_candidate', 'n_clicks_timestamp'),
               dash.dependencies.Input('next-button', 'n_clicks'),
               dash.dependencies.Input('next-button', 'n_clicks_timestamp')])
def update_user_classification_database(pics_value, pulsar_button, harmonic_button, rfi_button, class_a_button, class_b_button, n_clicks, next_button):


    user_classification = []
    
    pics_score_min = pics_value[0]
    pics_score_max = pics_value[1]
    dff = df[(df['pics_score_htru'] >= pics_score_min) & (df['pics_score_htru'] <= pics_score_max)]
    #dff = df3[(df3.pics_score_palfa >= pics_score_min) & (df3.pics_score_palfa <= pics_score_max)]

    dff = dff.reset_index()

    image_filename = dff['Cand Name'][n_clicks] # iterate over images
    pointing_name = dff['Pointing'][n_clicks]
    beam_number = dff['Beam'][n_clicks]
    dm_fraction = dff['DM-Frac'][n_clicks]


    if int(pulsar_button) > int(harmonic_button) and int(pulsar_button) > int(rfi_button) and int(pulsar_button) > int(next_button) and int(pulsar_button) > int(class_a_button) \
    and int(pulsar_button) > int(class_b_button):

        user_classification.append('vishnu' + ',' + str(datetime.datetime.now()) + ',' + image_filename + ',' + str(pointing_name) + ',' + str(beam_number) + ',' + str(dm_fraction) + ',' + '1' + '\n')          

    elif int(harmonic_button) > int(pulsar_button) and int(harmonic_button) > int(rfi_button) and int(harmonic_button) > int(next_button) and \
        int(harmonic_button) > int(class_a_button) and int(harmonic_button) > int(class_b_button):

        user_classification.append('vishnu' + ',' + str(datetime.datetime.now()) + ',' + image_filename + ',' + str(pointing_name) + ',' + str(beam_number) + ',' + str(dm_fraction) + ',' + '2' + '\n')

    elif int(rfi_button) > int(pulsar_button) and int(rfi_button) > int(harmonic_button) and int(rfi_button) > int(next_button) and int(rfi_button) > int(class_a_button) \
        and int(rfi_button) > int(class_b_button):

        user_classification.append('vishnu' + ',' + str(datetime.datetime.now()) + ',' + image_filename + ',' + str(pointing_name) + ',' + str(beam_number) + ',' + str(dm_fraction) + ',' + '3' + '\n')

    elif int(next_button) > int(pulsar_button) and int(next_button) > int(harmonic_button) and int(next_button) > int(rfi_button) and int(next_button) > int(class_a_button) \
        and int(next_button) > int(class_b_button):

        user_classification.append('vishnu' + ',' + str(datetime.datetime.now()) + ',' + image_filename + ',' + str(pointing_name) + ',' + str(beam_number) + ',' + str(dm_fraction) + ',' + '0' + '\n')

    elif int(class_a_button) > int(pulsar_button) and int(class_a_button) > int(harmonic_button) and int(class_a_button) > int(rfi_button) and \
        int(class_a_button) > int(next_button)  and int(class_a_button) > int(class_b_button):

        user_classification.append('vishnu' + ',' + str(datetime.datetime.now()) + ',' + image_filename + ',' + str(pointing_name) + ',' + str(beam_number) + ',' + str(dm_fraction) + ',' + '4' + '\n')
        cmds = 'cp ' +  png_path + image_filename + ' ' + png_path + 'selected/'
        subprocess.check_output(cmds, shell=True)


    elif int(class_b_button) > int(pulsar_button) and int(class_b_button) > int(harmonic_button) and int(class_b_button) > int(rfi_button) and \
        int(class_b_button) > int(next_button) and int(class_b_button) > int(class_a_button):

        user_classification.append('vishnu' + ',' + str(datetime.datetime.now()) + ',' + image_filename + ',' + str(pointing_name) + ',' + str(beam_number) + ',' + str(dm_fraction) + ',' + '5' + '\n')


    with open('user_classification_msp_cands_htru_retrained_after_topo_debacle.csv','a') as f:

        for item in user_classification:
            f.write("%s\n" % item)

        return None
#
@app.callback(dash.dependencies.Output('nearby-pulsar-table', 'rows'), 
             [dash.dependencies.Input('pics range', 'value'),
              dash.dependencies.Input('next-button', 'n_clicks')])
def update_known_pulsar_table(pics_value, next_button):


    pics_score_min = pics_value[0]
    pics_score_max = pics_value[1]
    dff = df[(df['pics_score_htru'] >= pics_score_min) & (df['pics_score_htru'] <= pics_score_max)]

    dff = dff.reset_index()

    image_filename = dff['Cand Name'][next_button] # iterate over images
    pointing_name = dff['Pointing'][next_button]
    beam_number = dff['Beam'][next_button]
    dff1 = df1[(df1.Pointing == pointing_name) & (df1.Beam == beam_number) & (df1['RAD.DISTANCE'] <= 1.0)]
    dff1 = dff1.sort_values('RAD.DISTANCE')
    dff1 = dff1.drop(['Pointing', 'Beam'], axis=1)
    return dff1.to_dict('records')

@app.callback(dash.dependencies.Output('container1', 'children'),
              [dash.dependencies.Input('pics range', 'value'),
               dash.dependencies.Input('pulsar-button', 'n_clicks_timestamp'),
               dash.dependencies.Input('harmonic-button', 'n_clicks_timestamp'),
               dash.dependencies.Input('rfi-button', 'n_clicks_timestamp'),
               dash.dependencies.Input('class_a_candidate', 'n_clicks_timestamp'),
               dash.dependencies.Input('class_b_candidate', 'n_clicks_timestamp'),
               dash.dependencies.Input('next-button', 'n_clicks'),
               dash.dependencies.Input('next-button', 'n_clicks_timestamp')])
def update_harmonics_on_screen(pics_value, pulsar_button, harmonic_button, rfi_button, class_a_button, class_b_button, n_clicks, next_button):

    msg = 'No Classifications Done Yet'

    pics_score_min = pics_value[0]
    pics_score_max = pics_value[1]
    dff = df[(df['pics_score_htru'] >= pics_score_min) & (df['pics_score_htru'] <= pics_score_max)]

    dff = dff.reset_index()
    if n_clicks > len(dff.index):
        msg = 'Congratulations! You are done with this beam!!'
        return html.Div([

        html.Div(msg)])
    else: 
        image_filename = dff['Cand Name'][n_clicks] # iterate over images
    
    
        spin_period = dff['Spin Period'][n_clicks]
        harmonics = []
        for harmonic in np.arange(2,10):
            harmonics.append(harmonic * spin_period)
        
        subharmonics = []
        for harmonic in np.arange(1,20):
            subharmonics.append(spin_period/harmonic)
        #msg = "Harmonics: %.3f,%.3f,%.3f,%.3f,%.3f,%.3f,%.3f," %(spin_period*2, spin_period*4, spin_period*8, spin_period*16, spin_period*32, spin_period*64, spin_period*128)    
        msg1 = "  ".join("%.3f"%x for x in harmonics)
        msg2 = "  ".join("%.3f"%x for x in subharmonics)
        msg = msg1 + ' fractional harm: ' + msg2


        return html.Div([

        html.Div(msg)

        ], style={'color': 'black', 'fontSize': 18})
#@app.callback(dash.dependencies.Output('ml_score1', 'children'),
#             [dash.dependencies.Input('pointing_dropdown', 'value'),
#              dash.dependencies.Input('beam_dropdown', 'value'),
#              dash.dependencies.Input('next-button', 'n_clicks')])
#def update_pics_score(pointing_name, beam_number, n_clicks):
#
#    if pointing_name is None:
#        return None
#    else:
#        if beam_number is None:
#            return None
#            #return make_table(dff, 'table')
#
#    dff = df2[(df2.POINTING == pointing_name) & (df2.BEAM == beam_number)]
#    dff = dff.reset_index()
#
#    #image_filename = dff['PNG_FILENAME'][n_clicks] # iterate over images
#    msg = 'PICS Score is: %s' %str(dff['pics_score_palfa'][n_clicks])
#
#    return html.Div([
#
#        html.Div(msg)
#
#        ], style={'color': 'black', 'fontSize': 18})



if __name__ == '__main__':
    app.run_server(debug=True)
