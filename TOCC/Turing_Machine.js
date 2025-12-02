class TuringMachine {
    constructor(tapeInput) {
        this.tape = tapeInput.split('');
        this.head = this.tape.length - 1; // Start at the rightmost bit (LSB)
        this.state = 'ADD'; // Initial State
        this.halted = false;
    }

    step() {
        if (this.halted) return;

        // If head moves beyond left boundary, prepend a blank/0
        if (this.head < 0) {
            this.tape.unshift('0');
            this.head = 0;
        }

        const currentVal = this.tape[this.head];

        if (this.state === 'ADD') {
            if (currentVal === '0') {
                this.tape[this.head] = '1'; // 0 + 1 = 1, no carry
                this.state = 'HALT';
            } else if (currentVal === '1') {
                this.tape[this.head] = '0'; // 1 + 1 = 0, carry 1
                this.head--; // Move Left
                // State remains ADD to process carry
            }
        } else if (this.state === 'HALT') {
            this.halted = true;
        }
    }

    run() {
        console.log(`Initial Tape: ${this.tape.join('')}`);
        let steps = 0;
        while (!this.halted && steps < 100) {
            this.step();
            if (this.state === 'HALT') this.halted = true;
            steps++;
        }
        console.log(`Final Tape:   ${this.tape.join('')}`);
    }
}
