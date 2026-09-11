async function loadJobs(){
 const r=await fetch("/api/jobs"); const jobs=await r.json();
 const s=document.getElementById("jobSelect");
 s.innerHTML=jobs.map(j=>`<option value="${j.id}">${j.title}</option>`).join("");
}
document.getElementById("jobForm").addEventListener("submit", async e=>{
 e.preventDefault(); const r=await fetch("/api/jobs",{method:"POST",body:new FormData(e.target)});
 if(r.ok){e.target.reset();await loadJobs();alert("Job created");}
});
async function screen(){
 const f=new FormData(); f.append("job_id",document.getElementById("jobSelect").value);
 const file=document.getElementById("resume").files[0]; if(!file)return alert("Select a resume");
 f.append("resume",file);
 document.getElementById("result").innerHTML="<p>Analyzing...</p>";
 const r=await fetch("/api/screen",{method:"POST",body:f}); const x=await r.json();
 if(!r.ok)return document.getElementById("result").innerHTML=`<p>${x.detail}</p>`;
 document.getElementById("result").innerHTML=`
 <div class="box"><div class="score">${x.score}%</div><h3>${x.candidate_name}</h3>
 <p><b>${x.recommendation}</b></p><p>${x.explanation}</p>
 <h4>Matched skills</h4>${(x.matched_skills||[]).map(s=>`<span class="pill">${s}</span>`).join("")}
 <h4>Missing skills</h4>${(x.missing_skills||[]).map(s=>`<span class="pill missing">${s}</span>`).join("")}
 <p><b>Experience:</b> ${x.experience_relevance}</p></div>`;
 document.getElementById("iresume").value=x.resume_text||"";
}
async function interview(){
 const f=new FormData();f.append("job_title",ititle.value);f.append("job_description",idesc.value);f.append("resume_text",iresume.value);f.append("difficulty",difficulty.value);
 const r=await fetch("/api/interview",{method:"POST",body:f});const x=await r.json();
 questions.innerHTML=(x.questions||[]).map(q=>`<li>${q}</li>`).join("");
}
async function uploadKnowledge(){
 const file=knowledgeFile.files[0];if(!file)return alert("Select a document");
 const f=new FormData();f.append("file",file);const r=await fetch("/api/knowledge",{method:"POST",body:f});const x=await r.json();
 knowledgeStatus.textContent=x.message||x.detail;
}
async function ask(){
 const f=new FormData();f.append("question",question.value);const r=await fetch("/api/ask",{method:"POST",body:f});const x=await r.json();answer.textContent=x.answer;
}
loadJobs();
