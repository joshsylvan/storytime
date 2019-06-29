export class SpeechBlock {
  constructor(lines) {
    this.lines = lines;
    this.currentLine = 0;
  }

  getCurrentLine() {
    return this.currentLine;
  }

  speek(callback) {
    const utterThis = new SpeechSynthesisUtterance(this.lines[this.currentLine]);
    utterThis.onend = () => {
      if (this.currentLine < this.lines.length) {
        this.currentLine++;
        this.speek();
      } else {
        if (callback) callback();
      }
    };
    window.speechSynthesis.speak(utterThis);
  }
};
