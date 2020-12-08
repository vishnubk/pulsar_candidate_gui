import dash
import dash_html_components as html
import dash_core_components as dcc
import dash_table
import dash_table_experiments as dt
import base64
import glob
import datetime
import numpy as np
import os, sys
import pandas as pd
import sys, subprocess
#png_path = '/media/8tb_drive/vishnu/ozstar_cands/msp_candidates_4bit_pics_retrained_renamed/'
''' Alpha 0.8- 1'''

#png_path = '/media/8tb_drive/vishnu/ozstar_cands/eta_0_8_and_1_renamed/'
#df = pd.read_csv('msp_search_candidates_alpha_above_0_8_below_1_4bit_4_Aug.csv', index_col=False, dtype={'Pointing':'str', 'Beam':'str', 'DM-Frac':'str', 'pfd_name':'str', 'Spin Period (ms)':np.float64, 'DM': np.float64})

''' Alpha below 0.8'''
png_path = '/media/8tb_drive/vishnu/ozstar_cands/eta_below_0_8_renamed/'
df = pd.read_csv('msp_search_candidates_alpha_below_0_8_4bit_4_Aug.csv', index_col=False, dtype={'Pointing':'str', 'Beam':'str', 'DM-Frac':'str', 'pfd_name':'str', 'Spin Period (ms)':np.float64, 'DM': np.float64})


''' SGAN '''

#png_path = '/media/8tb_drive/vishnu/ozstar_cands/msp_candidates_4bit_sgan_renamed/'
#df = pd.read_csv('msp_search_candidates_above_50_percent_sgan_4bit_4_Aug.csv', index_col=False, dtype={'Pointing':'str', 'Beam':'str', 'DM-Frac':'str', 'pfd_name':'str', 'Spin Period (ms)':np.float64, 'DM': np.float64})

''' PICS Re-trained '''
#png_path = '/media/8tb_drive/vishnu/ozstar_cands/msp_candidates_4bit_pics_retrained_renamed/'
#df = pd.read_csv('msp_search_candidates_above_50_percent_pics_retrained_4bit_4_Aug.csv', index_col=False, dtype={'Pointing':'str', 'Beam':'str', 'DM-Frac':'str', 'pfd_name':'str', 'Spin Period (ms)':np.float64, 'DM': np.float64})



''' eta below 0.8 OzSTAR'''
#png_path = '/media/8tb_drive/vishnu/ozstar_cands/eta_below_0_8_renamed_ozstar/'
#df = pd.read_csv('msp_search_candidates_alpha_below_0_8_4bit_9_Oct_ozstar.csv', index_col=False, dtype={'Pointing':'str', 'Beam':'str', 'DM-Frac':'str', 'pfd_name':'str', 'Spin Period (ms)':np.float64, 'DM': np.float64})

''' eta above 0.8 below 1 OzSTAR'''

#png_path = '/media/8tb_drive/vishnu/ozstar_cands/eta_0_8_and_1_renamed_ozstar/'
#df = pd.read_csv('msp_search_candidates_alpha_above_0_8_below_1_4bit_9_Oct_ozstar.csv', index_col=False, dtype={'Pointing':'str', 'Beam':'str', 'DM-Frac':'str', 'pfd_name':'str', 'Spin Period (ms)':np.float64, 'DM': np.float64})

''' SGAN OzSTAR '''
#png_path = '/media/8tb_drive/vishnu/ozstar_cands/msp_candidates_4bit_sgan_renamed_ozstar/'
#df = pd.read_csv('msp_search_candidates_above_50_percent_sgan_4bit_9_Oct_ozstar.csv', index_col=False, dtype={'Pointing':'str', 'Beam':'str', 'DM-Frac':'str', 'pfd_name':'str', 'Spin Period (ms)':np.float64, 'DM': np.float64})

#df = pd.read_csv('msp_search_candidates_above_50_percent_pics_retrained_4bit_4_Aug.csv', index_col=False, dtype={'Pointing':'str', 'Beam':'str', 'DM-Frac':'str', 'pfd_name':'str', 'Spin Period (ms)':np.float64, 'DM': np.float64})

folded_beams = pd.read_csv('beam_list_40_percent_lowlat_for_rahul.csv', index_col=False, dtype={'Pointing':'str', 'Beam':'str'})
df['Cand Name'] = df['pfd_name'].astype(str) + '.png' 

df1 = pd.read_csv('nearby_pulsars_htru_low_lat_pointings.csv', index_col=False, dtype={'Beam':'str', 'DM-Frac':'str'})
app = dash.Dash()
all_png_files = glob.glob(png_path + "*.png")
user_classification = pd.DataFrame(columns=['UserName','TimeStamp', 'ImageName', 'Pointing', 'Beam', 'Classification'])
if not os.path.exists('user_classification_40_percent_4bit.csv'):
    with open('user_classification_40_percent_4bit.csv', 'w') as outfile:
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

'''
Update Oct 2020
Give a priority beam list to view first. 
 #beam_list_40_percent.csv
'''

combined = pd.merge(df, folded_beams, how='inner', left_on=['Pointing','Beam'], right_on = ['Pointing','Beam'])
df = combined

df2 = pd.read_csv('user_classification_40_percent_4bit.csv', dtype={'Beam':'str', 'DM-Frac':'str'})
df3 = pd.merge(df, df2,  how='outer', left_on=['Pointing','Beam', 'DM-Frac', 'Cand Name'], right_on = ['Pointing','Beam', 'DM-Frac', 'ImageName'], indicator=True)
##df3 = df.merge(df2, left_on = 'Cand Name', right_on = 'ImageName', how='left', indicator=True)
#df4 = df3[df3["_merge"] == "left_only"].drop(columns=["_merge", "TimeStamp", "Classification", "Pointing_y", "Beam_y", "DM-Frac_y",  "UserName", "ImageName"])
df4 = df3[df3["_merge"] == "left_only"].drop(columns=["_merge", "TimeStamp", "Classification",  "UserName", "ImageName"])
#df4.columns = df.columns
#print(df.columns)
df = df4
#print('Total files: ', len(df.index))
#df = df.loc[(df['Spin Period (ms)'] >= 50) & (df['Sigma'] >= 7) & (df['Sigma'] <= 20)  & (df['DM'] >= 10)]

df = df.loc[(df['Spin Period (ms)'] >= 13) & (df['Spin Period (ms)'] <= 10000) & (df['Sigma'] >= 6) & (df['Sigma'] <= 20)  & (df['DM'] >= 10)]
#df = df.loc[(df['Spin Period (ms)'] >= 13) & (df['Spin Period (ms)'] <= 100) & (df['Sigma'] >= 9) & (df['DM'] >= 20)]
#df = df.loc[(df['Spin Period (ms)'] >= 10) & (df['Sigma'] >= 8) & (df['DM'] >= 20)]
#df = df.loc[(df['Spin Period (ms)'] >= 10) & (df['Spin Period (ms)'] <= 100)  & (df['DM'] >= 10)]
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

# Boostrap CSS.
#app.css.append_css({'external_url': 'https://codepen.io/amyoshino/pen/jzXypZ.css'})
app.css.append_css({'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css'})



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
    id='sgan range',
    marks={i: 'SGAN Score: {0:.1f}'.format(i) for i in pics_score},
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
    #id='nearby-pulsar-table'), style={'margin-left': -500, 'margin-right': 0, 'max-width': '3000px', 'overflow-x': 'scroll'}
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


@app.callback(dash.dependencies.Output('current-image', 'src'),
              [dash.dependencies.Input('sgan range', 'value'),
               dash.dependencies.Input('next-button', 'n_clicks')])
def update_image_src(value, next_button):

    

    pics_score_min = value[0]
    pics_score_max = value[1]
    dff = df[(df['sgan_score'] >= pics_score_min) & (df['sgan_score'] <= pics_score_max)]
    #dff = df[(df['pics_score_htru'] >= pics_score_min) & (df['pics_score_htru'] <= pics_score_max)]
    dff = dff.reset_index()

    image_filename = png_path + dff['Cand Name'][next_button] # iterate over images 
    encoded_image = base64.b64encode(open(image_filename, 'rb').read())
    return 'data:image/png;base64,{}'.format(encoded_image.decode())





@app.callback(dash.dependencies.Output('next-button', 'n_clicks'),
              [dash.dependencies.Input('sgan range', 'value')])
def reset_click_number(value):

    return None
#
#
@app.callback(dash.dependencies.Output('container', 'children'),
              [dash.dependencies.Input('sgan range', 'value'),
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
    dff = df[(df['sgan_score'] >= pics_score_min) & (df['sgan_score'] <= pics_score_max)]

    dff = dff.reset_index()
    if n_clicks > len(dff.index):
        msg = 'Congratulations! You are done with this beam!!'
        return html.Div([

        html.Div(msg)])
    else: 
        image_filename = dff['Cand Name'][n_clicks] # iterate over images
        current_sgan_score = float(dff['sgan_score'][n_clicks]) 
        current_pics_score = float(dff['pics_score_htru'][n_clicks]) 
    
    
        if int(pulsar_button) > int(harmonic_button) and int(pulsar_button) > int(rfi_button) and int(pulsar_button) > int(next_button) and int(pulsar_button) > int(class_a_button) \
        and int(pulsar_button) > int(class_b_button):
    
            #msg = '%s candidate is currently marked as a pulsar!!' %(image_filename)
            msg = '%s candidate is currently marked as a pulsar!! & SGAN Score is %.1f' %(image_filename, current_sgan_score)
 
        elif int(harmonic_button) > int(pulsar_button) and int(harmonic_button) > int(rfi_button) and int(harmonic_button) > int(next_button) and \
        int(harmonic_button) > int(class_a_button) and int(harmonic_button) > int(class_b_button):
    
            #msg = '%s candidate is currently marked as a harmonic!!' %(image_filename)
            msg = '%s candidate is currently marked as a harmonic!! & SGAN Score is %.1f' %(image_filename, current_sgan_score)

        elif int(rfi_button) > int(pulsar_button) and int(rfi_button) > int(harmonic_button) and int(rfi_button) > int(next_button) and int(rfi_button) > int(class_a_button) and \
        int(rfi_button) > int(class_b_button):
    
            #msg = '%s candidate is currently marked as RFI!!' %(image_filename)
            msg = '%s candidate is currently marked as RFI!! & SGAN Score is %.1f' %(image_filename, current_sgan_score)
    
        elif int(next_button) > int(pulsar_button) and int(next_button) > int(harmonic_button) and int(next_button) > int(rfi_button) and int(next_button) > int(class_a_button) and \
        int(next_button) > int(class_b_button):

            #msg = '%s candidate is currently marked as Noise!!' %(image_filename)
            msg = '%s candidate is currently marked as Noise!! & SGAN Score is %.1f & PICS Score is %.1f' %(image_filename, current_sgan_score, current_pics_score)

        elif int(class_a_button) > int(pulsar_button) and int(class_a_button) > int(harmonic_button) and int(class_a_button) > int(rfi_button) and \
        int(class_a_button) > int(next_button)  and int(class_a_button) > int(class_b_button):

            msg = '%s candidate is currently marked as Class A candidate. Yay!! & SGAN Score is %.1f' %(image_filename, current_sgan_score)
            cmds = 'cp ' +  png_path + image_filename + ' ' + png_path + 'ClassA_candidates/'
            subprocess.check_output(cmds, shell=True)

        elif int(class_b_button) > int(pulsar_button) and int(class_b_button) > int(harmonic_button) and int(class_b_button) > int(rfi_button) and \
        int(class_b_button) > int(next_button) and int(class_b_button) > int(class_a_button):

            msg = '%s candidate is currently marked as Class B candidate.!! & SGAN Score is %.1f' %(image_filename, current_sgan_score)
            cmds = 'cp ' +  png_path + image_filename + ' ' + png_path + 'ClassB_candidates/'
            subprocess.check_output(cmds, shell=True)

        return html.Div([

        html.Div(msg)

        ], style={'color': 'black', 'fontSize': 18})

@app.callback(dash.dependencies.Output('intermediate-classifications', 'children'),
              [dash.dependencies.Input('sgan range', 'value'),
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
    dff = df[(df['sgan_score'] >= pics_score_min) & (df['sgan_score'] <= pics_score_max)]
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

    elif int(class_b_button) > int(pulsar_button) and int(class_b_button) > int(harmonic_button) and int(class_b_button) > int(rfi_button) and \
        int(class_b_button) > int(next_button) and int(class_b_button) > int(class_a_button):

        user_classification.append('vishnu' + ',' + str(datetime.datetime.now()) + ',' + image_filename + ',' + str(pointing_name) + ',' + str(beam_number) + ',' + str(dm_fraction) + ',' + '5' + '\n')


    with open('user_classification_40_percent_4bit.csv','a') as f:

        for item in user_classification:
            f.write("%s\n" % item)

        return None
#
@app.callback(dash.dependencies.Output('nearby-pulsar-table', 'rows'), 
             [dash.dependencies.Input('sgan range', 'value'),
              dash.dependencies.Input('next-button', 'n_clicks')])
def update_known_pulsar_table(pics_value, next_button):


    pics_score_min = pics_value[0]
    pics_score_max = pics_value[1]
    dff = df[(df['sgan_score'] >= pics_score_min) & (df['sgan_score'] <= pics_score_max)]

    dff = dff.reset_index()

    image_filename = dff['Cand Name'][next_button] # iterate over images
    pointing_name = dff['Pointing'][next_button]
    beam_number = dff['Beam'][next_button]
    dff1 = df1[(df1.Pointing == pointing_name) & (df1.Beam == beam_number) & (df1['RAD.DISTANCE'] <= 1.0)]
    dff1 = dff1.sort_values('RAD.DISTANCE')
    dff1 = dff1.drop(['Pointing', 'Beam'], axis=1)
    return dff1.to_dict('records')

@app.callback(dash.dependencies.Output('container1', 'children'),
              [dash.dependencies.Input('sgan range', 'value'),
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
    dff = df[(df['sgan_score'] >= pics_score_min) & (df['sgan_score'] <= pics_score_max)]

    dff = dff.reset_index()
    if n_clicks > len(dff.index):
        msg = 'Congratulations! You are done with this beam!!'
        return html.Div([

        html.Div(msg)])
    else: 
        image_filename = dff['Cand Name'][n_clicks] # iterate over images
    
    
        spin_period = dff['Spin Period (ms)'][n_clicks]
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
