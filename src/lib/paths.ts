import type { CollectionEntry } from 'astro:content';
import { SITE } from '../config/site';

export type Article = CollectionEntry<'articles'>;

/** 'chlamydia/index' -> '/chlamydia/', 'chlamydia/symptoms-in-men' -> '/chlamydia/symptoms-in-men/' */
export function urlFor(id: string): string {
  const clean = id.replace(/(^|\/)index$/, '');
  return clean ? `/${clean}/` : '/';
}

export function sectionOf(id: string): string {
  return id.split('/')[0];
}

export function absolute(path: string): string {
  return new URL(path, SITE.url).toString();
}

export function formatDate(d: Date): string {
  return d.toLocaleDateString('en-US', { year: 'numeric', month: 'long', day: 'numeric', timeZone: 'UTC' });
}

export function isoDate(d: Date): string {
  return d.toISOString().slice(0, 10);
}

/** Sections that are not condition folders. */
export const SECTION_NAMES: Record<string, string> = {
  'std-testing': 'STD testing',
  guides: 'Guides',
};
