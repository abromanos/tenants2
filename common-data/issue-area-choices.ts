// This file was auto-generated by commondatabuilder.
// Please don't edit it.

export type IssueAreaChoice = "HOME"|"BEDROOMS"|"KITCHEN"|"LIVING_ROOM"|"BATHROOMS"|"PUBLIC_AREAS";

export const IssueAreaChoices: IssueAreaChoice[] = [
  "HOME",
  "BEDROOMS",
  "KITCHEN",
  "LIVING_ROOM",
  "BATHROOMS",
  "PUBLIC_AREAS"
];

const IssueAreaChoiceSet: Set<String> = new Set(IssueAreaChoices);

export function isIssueAreaChoice(choice: string): choice is IssueAreaChoice {
  return IssueAreaChoiceSet.has(choice);
}

export type IssueAreaChoiceLabels = {
  [k in IssueAreaChoice]: string;
};

export function getIssueAreaChoiceLabels(): IssueAreaChoiceLabels {
  return {
    HOME: "Entire home and hallways",
    BEDROOMS: "Bedrooms",
    KITCHEN: "Kitchen",
    LIVING_ROOM: "Living room",
    BATHROOMS: "Bathrooms",
    PUBLIC_AREAS: "Public areas",
  };
}
