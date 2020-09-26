import React from "react";
import Button from "react-bootstrap/Button";
import ButtonGroup from "react-bootstrap/ButtonGroup"
import Dropdown from "react-bootstrap/Dropdown"
import DropdownButton from "react-bootstrap/DropdownButton"
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faPlus, faMinus } from '@fortawesome/free-solid-svg-icons'
import patterns from "./data/patterns.json"

class Cell extends React.Component {
  render() {
    const color = this.props.color;
    const outerstyle = {
      overflow:'hidden',
      width: '16px',
      height: 'auto',
      backgroundColor: '#aaa',
      color:'red',
      borderColor: 'black'
    }
    const innerstyle = {
      color: color,
      border: "1px solid",
      backgroundColor: color,
      borderColor: color,
      height: 16,
      width: "auto"
    }
    return (
      <td style={outerstyle} onClick={this.props.handleClick}>
        <div style={innerstyle}></div>
      </td>
    )
  }
}

export class GameBoard extends React.Component {

  rows = 24;
  cols = 40;
  minDelay = 2;
  maxDelay = 10;

  constructor(props) {
    super(props);
    this.state = {
      birth: [3],
      survive: [2, 3],
      rulestring: "B2/S23",
      generation: 0,
      population: 0,
      running: false,
      delay: 4,
      // true represents a living cell, false a dead cell
      grid: Array(this.rows).fill().map(_ => Array(this.cols).fill(false)),
      prevGrid: Array(this.rows).fill().map(_ => Array(this.cols).fill(false))
    };
    // bind words to helper functions
    this.loadPattern = this.loadPattern.bind(this);
    this.setRule = this.setRule.bind(this);
    this.incrementDelay = this.incrementDelay.bind(this);
    this.toggleSimulation = this.toggleSimulation.bind(this);
    this.nextGeneration = this.nextGeneration.bind(this);
    this.handleClick = this.handleClick.bind(this);
    this.handleReset = this.handleReset.bind(this);
  }

  loadPattern(pattern) {
    this.handleReset();
    // midpoint of game board
    let mx = Math.floor(this.cols / 2);
    let my = Math.floor(this.rows / 2);
    // parse pattern rle
    let cells = [];
    let seglen = 1;
    let population = 0;
    for (let char of pattern.rle) {
      if (/^\d+$/.test(char)) {
        seglen = parseInt(char, 10);
      } else {
        if (char === 'b') {
          for (let i = 0; i < seglen; ++i) {
            cells.push(false);
          }
        } else if (char === 'o') {
          for (let i = 0; i < seglen; ++i) {
            cells.push(true);
            ++population;
          }
        }
        seglen = 1;
      }
    }
    // place pattern onto the grid
    let grid = this.state.grid;
    for (let x = 0; x < pattern.x; ++x) {
      for (let y = 0; y < pattern.y; ++y) {
        let i = (y * pattern.x) + x;
        let px = mx - Math.floor(pattern.x / 2);
        let py = my - Math.floor(pattern.y / 2);
        grid[py+y][px+x] = cells[i];
      }
    }
    this.setState({
      grid: grid,
      population: population
    })
  }

  setRule(rulestring) {
    let rules = rulestring.split("/");
    let birth = rules[0].split('').map(Number);
    let survive = rules[1].split('').map(Number);
    this.setState({
      birth: birth,
      survive: survive,
      rulestring: rulestring
    });
  }

  incrementDelay(increment) {
    let delay = this.state.delay;
    if ((increment > 0 && delay < this.maxDelay) || (increment < 0 && delay > this.minDelay)) {
      delay += increment;
      clearInterval(this.gameInterval);
      this.gameInterval = setInterval(() => {
        if (this.state.running) {
          this.nextGeneration();
        };
      }, delay * 100);
    }
    this.setState({
      delay: delay
    })
  }

  toggleSimulation() {
    let running = this.state.running;
    this.gameInterval = setInterval(() => {
      if (this.state.running) {
        this.nextGeneration();
      };
    }, this.state.delay * 100);
    console.log(this.gameInterval);
    this.setState({
      running: !running
    });
  }

  nextGeneration() {
    let grid = this.state.grid;
    let newGrid = this.state.prevGrid;
    let population = 0;
    for (let x = 0; x < this.rows; ++x) {
      for (let y = 0; y < this.cols; ++y) {
        let curcell = grid[x][y];
        let alive = 0;
        // offsets (Moore neighborhood)
        for (let dx = -1; dx <= 1; dx++) {
          for (let dy = -1; dy <= 1; dy++) {
            if (dx === 0 && dy === 0) { continue }
            else if (typeof grid[x+dx] !== 'undefined'
                && typeof grid[x+dx][y+dy] !== 'undefined'
                && grid[x+dx][y+dy]) {
                  alive++;
            }
          }
        }
        // if current cell is alive
        if (curcell && !this.state.survive.includes(alive)) {
          newGrid[x][y] = false;
        } else if (!curcell && this.state.birth.includes(alive)) {
          newGrid[x][y] = true;
        } else {
          newGrid[x][y] = curcell;
        }
        population += (newGrid[x][y] ? 1 : 0)
      }
    }
    this.setState({
      generation: this.state.generation + 1,
      population: population,
      grid: newGrid,
      prevGrid: grid
    });
  }

  // generate a new empty grid and set it to the grid state with setState
  handleReset() {
    let newGrid = Array(this.rows).fill().map(_ => Array(this.cols).fill(0));
    this.setState({
      generation: 0,
      population: 0,
      running: false,
      grid: newGrid
    });
  }

  handleClick(x, y) {
    let grid = this.state.grid;
    let population = this.state.population;
    grid[x][y] = !grid[x][y];
    population += 1 * (grid[x][y] ? 1 : -1)
    this.setState({
      generation: 0,
      population: population,
      running: false,
      grid: grid
    });
  }

  render() {
    const style = {
      textAlign: "center",
      margin: "auto",
      height: "auto",
      width: "500px",
      border: "1px solid black",
      tableLayout: 'fixed'
    };
    const grid = this.state.grid;
    const board = grid.map((row, i) => { return (
      <tr key={"row_" + i}>
        {row.map((_, j) => {
          const color = grid[i][j] ? "#111" : "#eee";
          const key = i + "_" + j;
          return (
            <Cell handleClick={() => this.handleClick(i, j)} color={color} key={key} />
          )
        })}
      </tr>)
    });

    return (<React.Fragment>
      <div className="d-flex flex-row">
        <DropdownButton id="ddl-patterns" title="Load Pattern">
            <Dropdown.Item onClick={() => this.loadPattern(patterns["glider"])}>Glider</Dropdown.Item>
            <Dropdown.Item onClick={() => this.loadPattern(patterns["blinker"])}>Blinker</Dropdown.Item>
            <Dropdown.Item onClick={() => this.loadPattern(patterns["beehive"])}>Beehive</Dropdown.Item>
            <Dropdown.Item onClick={() => this.loadPattern(patterns["rpentomino"])}>R-pentomino</Dropdown.Item>
            <Dropdown.Item onClick={() => this.loadPattern(patterns["pentadecathlon"])}>Pentadecathlon</Dropdown.Item>
            <Dropdown.Item onClick={() => this.loadPattern(patterns["lwss"])}>LWSS</Dropdown.Item>
        </DropdownButton>
        <DropdownButton id="ddl-rules" title="Set Rule">
            <Dropdown.Item onClick={() => this.setRule("B3/S23")}>Game of Life</Dropdown.Item>
            <Dropdown.Item onClick={() => this.setRule("B3/S12")}>Flock</Dropdown.Item>
            <Dropdown.Item onClick={() => this.setRule("B36/S125")}>2×2</Dropdown.Item>
            <Dropdown.Item onClick={() => this.setRule("B36/S23")}>HighLife</Dropdown.Item>
            <Dropdown.Item onClick={() => this.setRule("B37/S23")}>DryLife</Dropdown.Item>
            <Dropdown.Item onClick={() => this.setRule("B38/S23")}>Pedestrian Life</Dropdown.Item>
            <Dropdown.Item onClick={() => this.setRule("B3/S012345678")}>Inkspot</Dropdown.Item>
        </DropdownButton>
      </div>
      
      <table cellSpacing="0" style={style}>
        <tbody>
          {board}
        </tbody>
      </table>

      <ul className="list-inline">
        <li>{"Rule: " + this.state.rulestring}</li>
        <li>{"Generation: " + this.state.generation}</li>
        <li>{"Population: " + this.state.population}</li>
        <li>{"Speed: " + Math.round(10/this.state.delay * 100)/100 + " gens/s"}</li>
      </ul>

      <Button onClick={this.toggleSimulation}>{
        (this.state.running ? 'Stop' : 'Start') + " Simulation"
      }</Button>
      <Button onClick={this.nextGeneration} disabled={this.state.running}>Step</Button>
      <Button onClick={this.handleReset}>Reset Board</Button>
      <ButtonGroup aria-label="Basic example">
        <Button onClick={() => this.incrementDelay(2)} variant="secondary"><FontAwesomeIcon icon={faMinus} /></Button>
        <Button onClick={() => this.incrementDelay(-2)} variant="secondary">Speed <FontAwesomeIcon icon={faPlus} /></Button>
      </ButtonGroup>
    </React.Fragment>)
  }

}

export default GameBoard