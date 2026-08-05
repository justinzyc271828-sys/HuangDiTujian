import { useCallback, useEffect, useState } from "react";

const KEY = "hdtj-collection-v1";

type State = {
  read: string[];
  starred: string[];
};

function load(): State {
  try {
    const raw = localStorage.getItem(KEY);
    if (!raw) return { read: [], starred: [] };
    return JSON.parse(raw) as State;
  } catch {
    return { read: [], starred: [] };
  }
}

export function useCollection() {
  const [state, setState] = useState<State>(() => load());

  useEffect(() => {
    localStorage.setItem(KEY, JSON.stringify(state));
  }, [state]);

  const markRead = useCallback((id: string) => {
    setState((s) =>
      s.read.includes(id) ? s : { ...s, read: [...s.read, id] }
    );
  }, []);

  const toggleStar = useCallback((id: string) => {
    setState((s) => ({
      ...s,
      starred: s.starred.includes(id)
        ? s.starred.filter((x) => x !== id)
        : [...s.starred, id],
    }));
  }, []);

  return { ...state, markRead, toggleStar };
}
