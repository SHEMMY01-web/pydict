import React, { useState, useEffect } from 'react';
import { Award, CheckCircle2, XCircle, RotateCcw, ArrowRight, Sparkles, BookOpen } from 'lucide-react';
import { fetchQuiz } from '../services/api';

export default function QuizMode({ onSelectEntry }) {
  const [questions, setQuestions] = useState([]);
  const [currentIndex, setCurrentIndex] = useState(0);
  const [selectedOption, setSelectedOption] = useState(null);
  const [score, setScore] = useState(0);
  const [isAnswered, setIsAnswered] = useState(false);
  const [loading, setLoading] = useState(true);
  const [isCompleted, setIsCompleted] = useState(false);

  const loadQuiz = async () => {
    setLoading(true);
    setCurrentIndex(0);
    setSelectedOption(null);
    setScore(0);
    setIsAnswered(false);
    setIsCompleted(false);
    try {
      const data = await fetchQuiz();
      setQuestions(data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadQuiz();
  }, []);

  const handleSelectOption = (opt) => {
    if (isAnswered) return;
    setSelectedOption(opt);
    setIsAnswered(true);
    const currentQ = questions[currentIndex];
    if (opt === currentQ.correct_answer) {
      setScore((prev) => prev + 1);
    }
  };

  const handleNext = () => {
    if (currentIndex < questions.length - 1) {
      setCurrentIndex((prev) => prev + 1);
      setSelectedOption(null);
      setIsAnswered(false);
    } else {
      setIsCompleted(true);
    }
  };

  if (loading) {
    return (
      <div style={{ textAlign: 'center', padding: '6rem 2rem', color: 'var(--text-muted)' }}>
        <p style={{ fontSize: '1.2rem' }}>Generating Python Vocabulary Quiz...</p>
      </div>
    );
  }

  if (questions.length === 0) {
    return (
      <div className="quiz-card" style={{ textAlign: 'center' }}>
        <h2>Quiz Unavailable</h2>
        <p style={{ color: 'var(--text-secondary)' }}>Could not load questions. Try again shortly.</p>
        <button className="run-code-btn" onClick={loadQuiz}>
          <RotateCcw size={14} /> Retry
        </button>
      </div>
    );
  }

  if (isCompleted) {
    const percentage = Math.round((score / questions.length) * 100);

    return (
      <div className="quiz-card" style={{ textAlign: 'center', padding: '3rem 2rem' }}>
        <h2 style={{ fontSize: '1.6rem', fontWeight: 700, fontFamily: 'var(--font-serif)' }}>Quiz Result</h2>
        <p style={{ fontSize: '1.1rem', color: 'var(--text-secondary)', margin: '1rem 0 1.5rem 0' }}>
          You answered <strong>{score}</strong> out of <strong>{questions.length}</strong> questions correctly ({percentage}%).
        </p>

        <div style={{ display: 'flex', justifyContent: 'center', gap: '1rem' }}>
          <button className="wiki-action-btn" onClick={loadQuiz}>
            <RotateCcw size={14} />
            <span>Retake Quiz</span>
          </button>
        </div>
      </div>
    );
  }

  const currentQ = questions[currentIndex];

  return (
    <div className="quiz-card">
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', borderBottom: '1px solid var(--border-light)', paddingBottom: '0.85rem' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
          <Award size={18} color="var(--py-blue)" />
          <span style={{ fontWeight: 700, fontSize: '0.9rem', textTransform: 'uppercase', letterSpacing: '0.05em', color: 'var(--text-muted)' }}>
            Question {currentIndex + 1} of {questions.length}
          </span>
        </div>
        <span style={{ fontWeight: 700, fontFamily: 'var(--font-mono)', color: 'var(--py-blue)', fontSize: '0.95rem' }}>
          Score: {score}
        </span>
      </div>

      <div>
        <h3 style={{ fontSize: '1.25rem', fontWeight: 600, color: 'var(--text-main)', lineHeight: 1.5 }}>
          {currentQ.question}
        </h3>
      </div>

      <div style={{ display: 'flex', flexDirection: 'column', gap: '0.75rem' }}>
        {currentQ.options.map((opt) => {
          let btnClass = 'quiz-option-btn';
          if (isAnswered) {
            if (opt === currentQ.correct_answer) btnClass += ' correct';
            else if (opt === selectedOption) btnClass += ' wrong';
          }

          return (
            <button
              key={opt}
              className={btnClass}
              onClick={() => handleSelectOption(opt)}
              disabled={isAnswered}
            >
              <span>{opt}</span>
              {isAnswered && opt === currentQ.correct_answer && (
                <CheckCircle2 size={18} color="var(--emerald)" />
              )}
              {isAnswered && opt === selectedOption && opt !== currentQ.correct_answer && (
                <XCircle size={18} color="var(--rose)" />
              )}
            </button>
          );
        })}
      </div>

      {isAnswered && (
        <div style={{ background: 'var(--bg-subtle)', padding: '1.25rem', borderRadius: 'var(--radius-md)', display: 'flex', flexDirection: 'column', gap: '0.75rem', animation: 'fadeIn 200ms ease-out' }}>
          <div style={{ fontSize: '0.95rem', color: 'var(--text-secondary)' }}>
            <strong>Explanation:</strong> {currentQ.explanation}
          </div>

          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginTop: '0.5rem' }}>
            <button
              className="nav-btn"
              onClick={() => onSelectEntry(currentQ.term.toLowerCase())}
            >
              <BookOpen size={14} />
              <span>Inspect {currentQ.term} in Lexicon</span>
            </button>

            <button
              className="run-code-btn"
              onClick={handleNext}
            >
              <span>{currentIndex === questions.length - 1 ? 'Finish Quiz' : 'Next Question'}</span>
              <ArrowRight size={14} />
            </button>
          </div>
        </div>
      )}
    </div>
  );
}
