document.addEventListener('DOMContentLoaded', function(){
  const phrases = ['Dreamer', 'Tech Enthusiast', 'Traveller'];
  const el = document.getElementById('typed-placeholder');
  let idx = 0, char = 0, forward = true;

  function tick(){
    const word = phrases[idx];
    if(forward){
      char++;
      el.textContent = word.slice(0,char);
      if(char === word.length){
        forward = false;
        setTimeout(tick, 1200);
        return;
      }
    } else {
      char--;
      el.textContent = word.slice(0,char);
      if(char === 0){
        forward = true;
        idx = (idx+1) % phrases.length;
      }
    }
    setTimeout(tick, forward ? 120 : 60);
  }
  tick();
});
