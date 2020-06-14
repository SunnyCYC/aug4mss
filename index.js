let root_dir = 'Demo_mp3_15sec'
let song_titles = ['JoelHelander_ExcessiveResistancetoChange_p0_v0', 
'JoelHelander_ExcessiveResistancetoChange_p0_v1', 
'MatthewEntwistle_AnEveningWithOliver_p0_v0', 
'MatthewEntwistle_AnEveningWithOliver_p0_v1', 
'MatthewEntwistle_AnEveningWithOliver_p0_v2', 
'MatthewEntwistle_AnEveningWithOliver_p0_v3', 
'MatthewEntwistle_AnEveningWithOliver_p0_v4', 
'MatthewEntwistle_AnEveningWithOliver_p0_v5', 
'MatthewEntwistle_AnEveningWithOliver_p0_v6', 
'MatthewEntwistle_AnEveningWithOliver_p0_v7', 
'MatthewEntwistle_ImpressionsOfSaturn_p0_v0', 
'MatthewEntwistle_ImpressionsOfSaturn_p0_v1', 
'MatthewEntwistle_TheFlaxenField_p0_v0', 
'MatthewEntwistle_TheFlaxenField_p0_v1', 
'MutualBenefit_NotForNothing_p0_v0', 
'TheKitchenettes_Alive_p0_v0']

for( var i=0;i < song_titles.length;i++) {
    $('body').append(`

        <p>${song_titles[i]}</p>
        <ul>
            <li>
                <p>Mixture</p>
                <audio controls>
                    <source src="./${root_dir}/${song_titles[i]}.mp3" type="audio/mp3">
                </audio>
            </li>
            <li>
                <p>Random N2000 Estimates</p>
                violin
                <br>
                <audio controls>
                    <source src="./${root_dir}/${song_titles[i]}/Estimates/DR_ORI_n2000/violin.mp3" type="audio/mp3">
                </audio>
                <br>
                piano
                <br>
                <audio controls>
                    <source src="./${root_dir}/${song_titles[i]}/Estimates/DR_ORI_n2000/piano.mp3" type="audio/mp3">
                </audio>
            </li>
            <li>
                <p>Wet N2000 Estimates</p>
                violin
                <br>
                <audio controls>
                    <source src="./${root_dir}/${song_titles[i]}/Estimates/DR_Wet_n2000/violin.mp3" type="audio/mp3">
                </audio>
                <br>
                piano
                <br>
                <audio controls>
                    <source src="./${root_dir}/${song_titles[i]}/Estimates/DR_Wet_n2000/piano.mp3" type="audio/mp3">
                </audio>
            </li>
        </ul>
    `)
}