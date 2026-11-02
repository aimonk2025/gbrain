import { describe, test, expect } from "bun:test";
import { existsSync, readFileSync, readdirSync, statSync } from "fs";
import { join, relative } from "path";

const PACK_DIR = join(import.meta.dir, "..", "skills", "ca-pack");
const SKILLS_DIR = join(import.meta.dir, "..", "skills");
const pack: any = Bun.YAML.parse(readFileSync(join(PACK_DIR, "pack.yaml"), "utf-8"));
const manifest = JSON.parse(readFileSync(join(SKILLS_DIR, "manifest.json"), "utf-8"));
const manifestNames: string[] = manifest.skills.map((s: { name: string }) => s.name);
const onboardSkill = readFileSync(join(SKILLS_DIR, "onboard", "SKILL.md"), "utf-8");

/** Ops the onboard skill documents in its Phase 4 table. */
const DOCUMENTED_OPS = new Set(
  [...onboardSkill.matchAll(/^\| `([a-z_]+)` \|/gm)].map((m) => m[1]),
);

function walk(dir: string): string[] {
  const out: string[] = [];
  for (const e of readdirSync(dir)) {
    const p = join(dir, e);
    if (statSync(p).isDirectory()) out.push(...walk(p));
    else out.push(p);
  }
  return out;
}

describe("ca-pack manifest", () => {
  test("has identity fields", () => {
    expect(pack.pack).toBe("ca");
    expect(typeof pack.version).toBe("string");
    expect(pack.industry).toContain("accountancy");
  });

  test("every referenced file exists", () => {
    for (const f of Object.values(pack.reference as Record<string, string>)) {
      expect(existsSync(join(PACK_DIR, f))).toBe(true);
    }
    for (const c of pack.checklists) expect(existsSync(join(PACK_DIR, c.file))).toBe(true);
    for (const t of pack.templates) expect(existsSync(join(PACK_DIR, t.file))).toBe(true);
    for (const s of pack.skills) expect(existsSync(join(PACK_DIR, s.path))).toBe(true);
    expect(existsSync(join(PACK_DIR, pack.demo.dir))).toBe(true);
  });

  test("pack skills are registered in manifest.json", () => {
    for (const s of pack.skills) expect(manifestNames).toContain(s.id);
    expect(manifestNames).toContain("onboard");
  });

  test("service ids used by checklists, templates, skills, jobs and questions are defined", () => {
    const ids = new Set<string>(pack.services.map((s: any) => s.id));
    const check = (list: string[], where: string) => {
      for (const id of list) {
        if (id === "any") continue;
        expect(ids.has(id), `${where} references unknown service ${id}`).toBe(true);
      }
    };
    for (const c of pack.checklists) check(c.services, `checklist ${c.id}`);
    for (const t of pack.templates) check(t.services, `template ${t.id}`);
    for (const s of pack.skills) check(s.services, `skill ${s.id}`);
    for (const j of pack.jobs) check(j.services, `job ${j.id}`);
    const q = pack.questions.find((x: any) => x.id === "services");
    check(q.options, "question services.options");
    check(q.default, "question services.default");
  });

  test("calendar rows named by services exist in compliance-calendar.md", () => {
    const cal = readFileSync(join(PACK_DIR, pack.reference.calendar), "utf-8");
    const rows = new Set(
      cal.split("\n").filter((l) => l.startsWith("| ")).map((l) => l.split("|")[1].trim()),
    );
    for (const s of pack.services) {
      for (const r of s.calendar_rows) expect(rows.has(r), `calendar row "${r}" for ${s.id}`).toBe(true);
    }
  });

  test("question tree is well formed", () => {
    const ids = pack.questions.map((q: any) => q.id);
    expect(new Set(ids).size).toBe(ids.length);
    for (const q of pack.questions) {
      for (const d of q.depends_on ?? []) expect(ids, `${q.id} depends on unknown ${d}`).toContain(d);
      expect(q.title).toBeDefined();
      expect(q.type).toBeDefined();
      expect(Array.isArray(q.effects)).toBe(true);
      if (q.type === "single" && q.default && q.default !== "facts") {
        expect(q.options).toContain(q.default);
      }
      if (q.type === "multi" && Array.isArray(q.default)) {
        for (const d of q.default) expect(q.options).toContain(d);
      }
      if (q.default === undefined) expect(q.default_rule).toBeDefined();
    }
  });

  test("every effect op is documented in skills/onboard/SKILL.md", () => {
    expect(DOCUMENTED_OPS.size).toBeGreaterThan(5);
    for (const q of pack.questions) {
      for (const e of q.effects) expect(DOCUMENTED_OPS.has(e.op), `${q.id} uses undocumented op ${e.op}`).toBe(true);
    }
  });

  test("jobs name skills that exist", () => {
    for (const j of pack.jobs) {
      expect(manifestNames.includes(j.skill), `job ${j.id} names unknown skill ${j.skill}`).toBe(true);
    }
  });

  test("demo pages carry demo: true and the slug prefix", () => {
    const files = walk(join(PACK_DIR, pack.demo.dir)).filter((f) => f.endsWith(".md") && !f.endsWith("README.md"));
    expect(files.length).toBeGreaterThan(8);
    for (const f of files) {
      const body = readFileSync(f, "utf-8");
      expect(body.startsWith("---\n"), `${f} has no frontmatter`).toBe(true);
      expect(body, `${f} lacks demo: true`).toContain("\ndemo: true\n");
      const slug = relative(join(PACK_DIR, pack.demo.dir), f).replace(/\.md$/, "");
      const base = slug.split("/").pop()!;
      expect(base.startsWith(pack.demo.slug_prefix), `${slug} lacks prefix`).toBe(true);
    }
  });

  test("demo queries point at demo pages that exist", () => {
    for (const q of pack.demo.queries) {
      const target = q.expect ?? q.input ?? q.slug;
      expect(existsSync(join(PACK_DIR, pack.demo.dir, `${target}.md`)), `demo target ${target}`).toBe(true);
    }
  });

  test("example answers file matches the schema's required keys and question ids", () => {
    const schema = JSON.parse(readFileSync(join(SKILLS_DIR, "onboard", "answers.schema.json"), "utf-8"));
    const example = JSON.parse(readFileSync(join(SKILLS_DIR, "onboard", "examples", "answers.ca.json"), "utf-8"));
    for (const k of schema.required) expect(example, `missing ${k}`).toHaveProperty(k);
    const qids = new Set(pack.questions.map((q: any) => q.id));
    for (const k of Object.keys(example.answers)) expect(qids.has(k), `answer for unknown question ${k}`).toBe(true);
    for (const k of example.skipped ?? []) expect(qids.has(k)).toBe(true);
    expect(example.pack).toBe(pack.pack);
  });
});
