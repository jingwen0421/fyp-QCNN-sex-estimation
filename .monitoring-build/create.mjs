import fs from 'node:fs/promises';
import {createRequire} from 'node:module';
import {pathToFileURL} from 'node:url';
const rt='C:/Users/jwenn/.cache/codex-runtimes/codex-primary-runtime/dependencies';
const req=createRequire(rt+'/node/node_modules/runtime.cjs');
const {Presentation,PresentationFile}=await import(pathToFileURL(req.resolve('@oai/artifact-tool')).href);
const p=Presentation.create({slideSize:{width:1280,height:720}});
const ink='#153D3C', teal='#08766F', muted='#47625F';
function text(s,v,x,y,w,h,size,bold=false,color=ink){
 const q=s.shapes.add({geometry:'textbox',position:{left:x,top:y,width:w,height:h},fill:'none',line:{fill:'none',width:0}});
 q.text=v; q.text.style={typeface:'Aptos',fontSize:size,bold,color,verticalAlignment:'middle',insets:{left:0,right:0,top:0,bottom:0}};
}
function slide(title,sub,notes){
 const s=p.slides.add(); s.background.fill='#F4F8F7';
 text(s,title,80,55,1120,74,50,true); text(s,sub,80,133,1120,48,26,false,muted);
 s.speakerNotes.text=notes; return s;
}
function rows(s,data){data.forEach(([label,value],i)=>{
 const y=211+i*103;
 text(s,label,80,y,335,76,29,true,teal); text(s,value,430,y,770,76,29);
});}
function table(s,data){
 const t=s.tables.add({rows:data.length,columns:3,left:80,top:205,width:1120,height:data.length*56,columnWidths:[480,320,320],values:data});
 t.borders.assign({style:'solid',fill:'#D5E6E2',width:1});
 data.forEach((r,i)=>r.forEach((_,j)=>{
  const c=t.getCell(i,j);c.fill=i===0?'#DDEEE9':i%2?'#FFFFFF':'#F4F8F7';
  c.text.style={typeface:'Aptos',fontSize:25,bold:i===0,color:ink};
 }));
}
{
 const s=p.slides.add();s.background.fill='#E8F3EF';
 text(s,'FYP II   /   WEEK 7 MONITORING',80,111,1120,43,24,true,teal);
 text(s,'Investigation of Sexual Dimorphism in\nOrbital and Nasal Morphology Using QCNN',80,205,1120,165,50,true);
 text(s,'Wong Jing Wen  ·  23004924',80,435,1120,48,29,true);
 text(s,'Supervisor: Dr. Erma Rahayu Mohd Faizal',80,490,1120,48,27,false,muted);
 s.speakerNotes.text='I am comparing a quantum convolutional neural network with classical models and building CranioLab to demonstrate sex estimation. Title and author details are from FYP Monitoring Slides.pdf. Monitoring schedule is from AP BRIEFING 2026.pdf, pages 13–16 and 24.';
}
rows(slide('Project scope and progress','Sex estimation from orbital and nasal measurements','Explain that the scope follows the Female and Male labels in the study data. Progress is an informal technical estimate excluding the report.'),[
 ['Data and collaboration','Completed collaborator registration and data cleaning. The study dataset has 1,042 records.'],
 ['Model development','Evaluated four classical baselines and the initial QCNN. Completed readout, learning-rate and ablation experiments.'],
 ['CranioLab prototype','Built a Streamlit interface with manual entry, dataset upload and an evaluation view.'],
 ['Technical progress','Estimated 75–80% complete, excluding the report.']
]);
rows(slide('Data and evaluation setup','The split keeps identical measurement groups together','Explain how identical feature patterns crossing train and test could distort evaluation. Macro F1 averages the F1 scores for Female and Male equally. Sources: notebooks 04–08 and 10.'),[
 ['Eight inputs','Six orbital and two nasal measurements.'],
 ['Class distribution','587 Male and 455 Female records. Macro F1 gives equal weight to the two classes.'],
 ['Development set','664 fitting and 168 validation records. The scaler uses fitting records during QCNN tuning.'],
 ['Shared test set','210 records for the initial model comparison.']
]);
table(slide('Classical baselines lead the initial QCNN','Shared test split of 210 records','Logistic regression has the highest accuracy and macro F1 in this comparison. QCNN is the original fixed-average model. Source: results/logistic_regression_baseline/model_comparison.csv.'),[
 ['Model','Accuracy','Macro F1'],['Logistic regression','80.48%','79.98%'],['CNN','80.00%','79.32%'],['XGBoost','79.05%','78.41%'],['MLP','71.43%','70.56%'],['Initial QCNN','69.05%','68.36%']
]);
rows(slide('QCNN experiments','Three seeds on the same 168 validation records','The readout combines the four measured circuit outputs into a score. Each sigmoid run selected epoch 29 under a 30-epoch cap. Sources: notebooks 05, 06, 08 and 10.'),[
 ['Learned readout','Improved validation macro F1 over the fixed average at all three seeds.'],
 ['Learning rate','0.01 and 0.02 produced nearly identical mean validation macro F1.'],
 ['Sigmoid readout','72.41% mean validation macro F1 and 73.02% mean validation accuracy.'],
 ['Feature ablation','Macro F1 was 72.41% with all eight inputs, 71.73% with nasal only and 61.62% with orbital only.']
]);
{
 const s=slide('Performance by recorded ethnicity','Initial QCNN on the shared test split','The subgroup results are descriptive. Independent cross-population evaluation remains future work. Source: results/ethnicity_evaluation/subgroup_metrics.csv.');
 table(s,[['Recorded ethnicity','Correct / records','Accuracy'],['Chinese','58 / 74','78.38%'],['Indian','32 / 52','61.54%'],['Malay','55 / 84','65.48%']]);
 text(s,'Subgroup sizes differ. These results describe variation within the Malaysian dataset.',80,477,1120,64,26,false,muted);
}
rows(slide('CranioLab demo','Manual sex estimation in the Streamlit prototype','Switch to the running app here. Use a prepared example without a case identifier. The current deployment uses the original fixed-average QCNN. Sources: app.py and qcnn_inference.py.'),[
 ['Enter a case','Type eight measurements in millimetres in the Sex estimation tab.'],
 ['Run an estimate','Show the predicted class from the original QCNN.'],
 ['Review results','Open Evaluation to show the saved model metrics.'],
 ['Final integration','Connect the selected QCNN and verify manual entry and upload end to end.']
]);
rows(slide('Next steps and supervisor feedback','','Ask which statistical comparison matters most and what user testing evidence is expected. Record the meeting and feedback in Ilmiah. AP BRIEFING 2026.pdf, pages 19 and 24.'),[
 ['Final model','Compare 30 and 60 epochs, select by validation macro F1, then evaluate on the shared test split.'],
 ['System testing','Integrate the selected model and plan user acceptance testing.'],
 ['Research priority','Which statistical comparison matters most: QCNN vs. the strongest baseline, or learned vs. fixed readout?'],
 ['Demo scope','Should the app offer baseline selection? Who should take part in user testing?']
]);
const root=process.cwd(), build=root+'/.monitoring-build';
await fs.mkdir(root+'/monitoring',{recursive:true});
for(const [i,s] of p.slides.items.entries()){
 const png=await p.export({slide:s,format:'png',scale:0.75});
 await fs.writeFile(build+'/slide-'+(i+1)+'.png',new Uint8Array(await png.arrayBuffer()));
}
const draft=build+'/candidate.pptx';
await (await PresentationFile.exportPptx(p)).save(draft);
const sk='C:/Users/jwenn/.codex/plugins/cache/openai-primary-runtime/presentations/26.1111.10930/skills/presentations/container_tools';
const {finalizePresentation}=await import(pathToFileURL(sk+'/artifact_tool_utils.mjs').href);
await finalizePresentation({workspaceDir:root,candidatePath:draft,finalPath:root+'/monitoring/FYP II Monitoring - Wong Jing Wen.pptx',pythonExecutable:rt+'/python/python.exe',integrityValidatorPath:sk+'/inspect_presentation_package_integrity.py',layoutValidatorPath:sk+'/inspect_presentation_layout_geometry.py',layoutArgs:['--expected-slide-size-emu','12192000,6858000','--validate-heading-fit','--require-native-table-slide','4','--require-native-table-slide','6'],requiredNativeTableOwnerSlides:[4,6],fontPolicy:{basis:'design',families:['Aptos']},verifyArtifactToolImport:true,receiptPath:build+'/validation.json'});
