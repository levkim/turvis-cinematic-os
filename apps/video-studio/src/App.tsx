import { useMemo, useState } from 'react';

type Category = {
  id: string;
  label: string;
  description: string;
  defaultDuration: number;
  aspect: string;
};

const categories: Category[] = [
  { id: 'documentary', label: '다큐멘터리', description: '서사와 정보가 있는 영상', defaultDuration: 240, aspect: '16:9' },
  { id: 'cinematic', label: '시네마틱', description: '감성, 풍경, 분위기 중심 영상', defaultDuration: 180, aspect: '16:9' },
  { id: 'promotion', label: '홍보 영상', description: '상품, 서비스, 장소 홍보 영상', defaultDuration: 90, aspect: '16:9' },
  { id: 'education', label: '교육 영상', description: '강의, 안전교육, 절차 설명 영상', defaultDuration: 300, aspect: '16:9' },
  { id: 'youtube', label: '유튜브', description: '유튜브 업로드용 일반 영상', defaultDuration: 480, aspect: '16:9' },
  { id: 'shorts-reels', label: '쇼츠 / 릴스', description: '짧은 세로형 숏폼 영상', defaultDuration: 45, aspect: '9:16' },
  { id: 'corporate', label: '기업 / 기관 영상', description: '회사, 기관, 관광청, 조직 PR', defaultDuration: 120, aspect: '16:9' },
  { id: 'interview', label: '인터뷰', description: '인물, 전문가, 증언 중심 영상', defaultDuration: 300, aspect: '16:9' },
  { id: 'presentation', label: '프레젠테이션', description: '발표, 제안, 브리핑 영상', defaultDuration: 180, aspect: '16:9' },
  { id: 'custom', label: '커스텀', description: '직접 목적과 스타일을 정의', defaultDuration: 180, aspect: '16:9' },
];

function slugify(value: string): string {
  return value
    .trim()
    .toLowerCase()
    .replace(/[^a-z0-9가-힣]+/g, '-')
    .replace(/-+/g, '-')
    .replace(/^-|-$/g, '') || 'new-video';
}

export function App() {
  const [title, setTitle] = useState('새 영상 프로젝트');
  const [categoryId, setCategoryId] = useState('cinematic');
  const selectedCategory = categories.find((category) => category.id === categoryId) || categories[1];
  const [projectId, setProjectId] = useState('new-video');
  const [duration, setDuration] = useState(selectedCategory.defaultDuration);
  const [aspect, setAspect] = useState(selectedCategory.aspect);
  const [narration, setNarration] = useState('');

  const commands = useMemo(() => {
    const safeId = slugify(projectId || title);
    return {
      create: `python apps/turvis-studio/turvis.py create --title "${title}" --id ${safeId} --category ${categoryId} --duration ${duration} --aspect "${aspect}"`,
      fastDraft: `python apps/turvis-studio/turvis.py fast-draft --project-folder projects/${safeId}`,
      preview: 'python apps/turvis-studio/turvis.py preview',
      narrationPath: `projects/${safeId}/narration.md`,
    };
  }, [aspect, categoryId, duration, projectId, title]);

  const handleCategoryChange = (nextId: string) => {
    const nextCategory = categories.find((category) => category.id === nextId) || categories[1];
    setCategoryId(nextId);
    setDuration(nextCategory.defaultDuration);
    setAspect(nextCategory.aspect);
  };

  return (
    <main className="studio-shell">
      <section className="hero">
        <div>
          <p className="eyebrow">TURVIS VIDEO STUDIO</p>
          <h1>New Video Wizard</h1>
          <p className="hero-copy">영상 종류를 고르고, 제목과 나레이션을 넣은 뒤 빠른 초안을 생성합니다.</p>
        </div>
        <div className="status-card">
          <span>Fast Draft</span>
          <strong>Ready</strong>
        </div>
      </section>

      <section className="layout-grid">
        <div className="panel category-panel">
          <div className="panel-header">
            <p className="step">STEP 1</p>
            <h2>영상 종류</h2>
          </div>
          <div className="category-grid">
            {categories.map((category) => (
              <button
                key={category.id}
                className={category.id === categoryId ? 'category-card active' : 'category-card'}
                onClick={() => handleCategoryChange(category.id)}
              >
                <strong>{category.label}</strong>
                <span>{category.description}</span>
              </button>
            ))}
          </div>
        </div>

        <div className="panel form-panel">
          <div className="panel-header">
            <p className="step">STEP 2</p>
            <h2>프로젝트 정보</h2>
          </div>

          <label>
            제목
            <input value={title} onChange={(event) => setTitle(event.target.value)} />
          </label>

          <label>
            프로젝트 ID
            <input value={projectId} onChange={(event) => setProjectId(event.target.value)} />
          </label>

          <div className="two-cols">
            <label>
              길이(초)
              <input type="number" value={duration} onChange={(event) => setDuration(Number(event.target.value))} />
            </label>
            <label>
              화면비
              <select value={aspect} onChange={(event) => setAspect(event.target.value)}>
                <option value="16:9">16:9</option>
                <option value="9:16">9:16</option>
                <option value="1:1">1:1</option>
                <option value="4:5">4:5</option>
              </select>
            </label>
          </div>

          <label>
            나레이션 초안
            <textarea
              value={narration}
              onChange={(event) => setNarration(event.target.value)}
              placeholder="여기에 나레이션을 붙여넣으세요. 현재 버전은 파일에 직접 붙여넣고 명령을 실행합니다."
            />
          </label>
        </div>

        <div className="panel command-panel">
          <div className="panel-header">
            <p className="step">STEP 3</p>
            <h2>실행 순서</h2>
          </div>
          <ol className="command-list">
            <li>
              <span>프로젝트 생성</span>
              <code>{commands.create}</code>
            </li>
            <li>
              <span>나레이션 붙여넣기</span>
              <code>{commands.narrationPath}</code>
            </li>
            <li>
              <span>빠른 초안 생성</span>
              <code>{commands.fastDraft}</code>
            </li>
            <li>
              <span>프리뷰</span>
              <code>{commands.preview}</code>
            </li>
          </ol>
          <p className="note">다음 개발 단계에서 이 명령들을 버튼 클릭으로 직접 실행하게 연결합니다.</p>
        </div>
      </section>
    </main>
  );
}
